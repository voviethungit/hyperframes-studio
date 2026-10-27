import json,re,unicodedata,difflib,hashlib,os
from pathlib import Path
T=float(json.load(open('work/probe.json'))['format']['duration'])
a=json.load(open(os.environ.get('ASR_INPUT','work/asr.json'))); assert a['complete'] or os.environ.get('PILOT')
if os.environ.get('PILOT'):T=a['segments'][-1]['end']
flat=[]
for chunk in a['segments']:
 raw=json.loads(chunk['raw_result'])
 for st,dur,txt in zip(raw['segment_timestamps'],raw['segment_durations'],raw['segment_texts']):
  flat.append({'start':chunk['start']+st,'end':min(T,chunk['start']+st+dur),'text':txt,'words':[],'confidence':None,'boundary_confidence':'lower; Whisper timestamp tokens, not forced-aligned','boundary_method':'Whisper segment timestamps within waveform-bounded chunk'})
a['segments']=flat
def norm(s):return re.sub(r'[^a-z0-9 ]','',unicodedata.normalize('NFKD',s.lower()).encode('ascii','ignore').decode()).split()
script=Path('guion_01_es.txt').read_text();spoken=' '.join(s['text'] for s in a['segments']);sw=norm(script);aw=norm(spoken)
diff=[{'operation':tag,'script':' '.join(sw[i:j]),'spoken':' '.join(aw[k:l]),'script_word_range':[i,j],'asr_word_range':[k,l]} for tag,i,j,k,l in difflib.SequenceMatcher(None,sw,aw,autojunk=False).get_opcodes() if tag!='equal']
a.update({'duration':T,'method':'sherpa-onnx Whisper base int8 Spanish, greedy decode, segment timestamp tokens; no word alignment','boundary_precision':'ASR estimates, not manually verified; low-probability words require review','discrepancies':diff,'script_similarity':difflib.SequenceMatcher(None,sw,aw,autojunk=False).ratio()})
json.dump(a,open('output/audio_alignment.json','w'),ensure_ascii=False,indent=2)
Path('output/transcript_es.txt').write_text(spoken)
# Ordered semantic milestones are located in actual recognized speech, never a proportional script split.
anchors=[('cow','abres los ojos'),('village','sales corriendo del establo'),('reveal','has viajado'),('village','tu estomago'),('breakfast','primero el desayuno'),('field','sales al campo'),('sickle','levantas la hoz'),('field','la anciana se acerca'),('official','hombre bien vestido'),('field','continuas trabajando'),('bundle','formar haces'),('water','tu boca esta seca'),('breakfast','finalmente llega la comida'),('storm','escuchas un trueno'),('mud','agarras el primero'),('cart','una de sus ruedas'),('bundle','todavia queda trabajo'),('walk','cuando termina el trabajo'),('stores','no todo el grano'),('dinner','finalmente regresas'),('sleep','cuando llega la hora'),('morning','a la manana siguiente'),('final','entonces aparece el campesino')]
words=[{'word':s['text'],'start':s['start']} for s in a['segments']]; nt=[]; origins=[]
for w in words:
 for z in norm(w['word']):nt.append(z);origins.append(w['start'])
marks=[(0,'cow')];cursor=0
for typ,phrase in anchors:
 q=norm(phrase);found=None
 for i in range(cursor,len(nt)-len(q)+1):
  if nt[i:i+len(q)]==q or difflib.SequenceMatcher(None,' '.join(nt[i:i+len(q)]),' '.join(q)).ratio()>=.88:found=i;break
 if found is not None:
  if origins[found]>0.5:marks.append((origins[found],typ))
  cursor=found+len(q)
marks=sorted(set(marks));scenes=[]
for i,s in enumerate(a['segments']):
 start=0 if i==0 else s['start'];end=a['segments'][i+1]['start'] if i+1<len(a['segments']) else T
 typ=next(v for st,v in reversed(marks) if st<=start)
 text=s['text'].strip();n=' '.join(norm(text))
 pose='cut' if typ in ['field','sickle'] else 'carry' if typ=='bundle' else 'stand'
 if any(k in n for k in ['te agachas','agacharte']):pose='bend'
 if any(k in n for k in ['bebes','bebiendo']):pose='drink'
 if any(k in n for k in ['muerdes','masticas','bocado','mientras cenas']):pose='eat'
 if any(k in n for k in ['senala','levantas la mano']):pose='point'
 emotion='exhausted' if any(z in n for z in ['agotado','duele','cans','tiembl','barro']) else 'scared' if any(z in n for z in ['peligro','trueno','pum','plof']) else 'confident' if any(z in n for z in ['conseguiste','sonries','funciona']) else 'confused'
 label=''
 for key,l in [('nadie bebia agua','EL AGUA: UN MITO'),('eso es falso','SÍ BEBÍAN AGUA'),('franjas','CAMPOS ABIERTOS'),('obligaciones','OBLIGACIONES SEÑORIALES'),('futuras siembras','RESERVAS PARA SEMBRAR'),('veinticuatro horas','24 HORAS'),('era su vida','ERA SU VIDA')]:
  if key in n:label=l;break
 scenes.append({'id':i,'start':start,'end':end,'audio_text':text,'matching_script_text':difflib.get_close_matches(text,script.splitlines(),1,.45),'type':typ,'pose':pose,'emotion':emotion,'shot':('close' if any(z in n for z in ['te mira','lo miras','tu sonrisa','quedas inmovil','cierras los ojos','abres un ojo','tu mandibula']) else 'medium' if pose in ['eat','drink','cut','bend'] else 'wide'),'label':label,'action':'release' if typ=='cart' and any(z in n for z in ['sale del barro','lo conseguiste']) else 'perform','visual_beat':{'location':typ,'action':text,'method':'layered SVG rig, deterministic keyframes and procedural environment','camera':'wide action composition','transition':'cut at ASR phrase boundary'},'diagram':(['SEMBRAR','COSECHAR','MOLER','HORNEAR'] if any(k in n for k in ['sembrarlo','molerse','hornearla','preparar la masa']) else ['FUENTE','RECIPIENTE','TRANSPORTE','FUEGO'] if typ=='water' and any(k in n for k in ['transport','calentar','combustible','llenar']) else None),'props':{'cow':['cow','straw'],'sickle':['sickle','grain'],'water':['well','bucket'],'cart':['cart','grain bundles','boards'],'dinner':['bowl','hearth'],'sleep':['straw','mouse']}.get(typ,['period environment']),'sfx':[],'state':{'hero_id':'hero-01','facing':'right','scarf':'golden yellow','hair':'black 70/30','weather':'rain' if typ in ['storm','mud','cart'] else 'clear','completed_actions':[],'continuity_status':'procedural layout; paragraph cut continuity requires editorial review'}})
completed=[]
for s in scenes:
 n=' '.join(norm(s['audio_text']))
 if s['type']=='mud':
  if any(z in n for z in ['resbalas','plof','plove','caes de espaldas']):s['action']='fall'
  elif 'te levantas' in n:s['action']='rise'
  if s['action']=='rise' and 'mud_fall' not in completed:completed.append('mud_fall')
  s['state']['mud_fallen']='mud_fall' in completed and 'mud_rise' not in completed
  if s['action']=='fall' and 'mud_fall' not in completed:completed.append('mud_fall')
  if s['action']=='rise' and 'mud_rise' not in completed:completed.append('mud_rise')
 if s['type']=='cart':
  s['state']['cart_released']='cart_release' in completed
  if s['action']=='release' and 'cart_release' not in completed:completed.append('cart_release')
 s['state'].update({'completed_actions':completed.copy(),'hero_position_reference':[620,810],'eyeline':'task or nearby farmer','pose':s['pose'],'prop_ownership':{'sickle':'hero' if s['type'] in ['field','sickle','final'] else 'not established'},'time_of_day':'night' if s['type']=='sleep' else 'evening' if s['type']=='dinner' else 'day'})
for s in scenes:
 s['visual_beat']['camera']=s['shot']
 s['state']['hero_position_reference']=[620,900 if s['type'] in ['breakfast','dinner'] else 810]
 s['state']['position_precision']='reference only; action paths are evaluated per frame in renderer'
 if s['type']=='cow':s['state']['position_path']='x=790→420, y=850; roll left at 5.88 s, hoof impact at 9.32 s'
 elif s['type']=='mud':s['state']['position_path']='x=750; fall at actual phrase onset, y=810→850; rise uses phrase progress'
 elif s['type']=='sleep':s['state']['hero_position_reference']=[640,850]
 elif s['type'] in ['walk','village']:s['state']['position_path']='x=500+500×section progress, y=810'
 elif s['type']=='cart':s['state']['position_path']='x=820+push displacement; cart release tracked separately'
json.dump({'duration':T,'fps':30,'scenes':scenes,'milestones':marks},open('output/scene_plan.json','w'),ensure_ascii=False,indent=2)
json.dump([{'scene':s['id'],**s['state']} for s in scenes],open('output/scene_state.json','w'),ensure_ascii=False,indent=2)
def stamp(t,sep):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{s:02}{sep}{ms:03}'
cues=[]
for seg in a['segments']:
 ws=seg['words'];chunk=[]
 if not ws:
  cues.append((seg['start'],seg['end'],seg['text'].strip()))
  continue
 for w in ws:
  chunk.append(w)
  if len(''.join(x['word'] for x in chunk))>68 or w is ws[-1]:
   cues.append((chunk[0]['start'],chunk[-1]['end'],''.join(x['word'] for x in chunk).strip()));chunk=[]
Path('output/subtitles_es.srt').write_text('\n\n'.join(f'{i+1}\n{stamp(st,",")} --> {stamp(en,",")}\n{tx}' for i,(st,en,tx) in enumerate(cues))+'\n')
Path('output/subtitles_es.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{stamp(st,".")} --> {stamp(en,".")}\n{tx}' for st,en,tx in cues)+'\n')
print(len(scenes),'scenes',len(words),'words',len(diff),'differences',marks)
