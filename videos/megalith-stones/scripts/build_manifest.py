"""Build the complete editorial manifest from acoustic alignment and authored shots.

No HeyGen call is simulated. Audio is read for analysis, never rewritten.
"""
import csv, hashlib, html, io, json, re, subprocess, zipfile, difflib, statistics, os
from collections import Counter
from pathlib import Path

ROOT=Path(os.environ.get('MEGALITH_PROJECT_DIR',Path(__file__).resolve().parents[1]))
OUT=ROOT/'deliverables'
AUDIO=Path(os.environ.get('MEGALITH_AUDIO',ROOT/'private/voice.mp3'))
SCRIPT=Path(os.environ.get('MEGALITH_SCRIPT',ROOT/'private/source-script.txt'))
MODEL=Path(os.environ.get('MEGALITH_MODEL_DIR',ROOT/'models/sherpa-onnx-nemo-ctc-giga-am-v2-russian-2025-04-19'))
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(AUDIO)]))
DURATION=float(probe['format']['duration'])
phrases=json.loads((OUT/'phrase-alignment.json').read_text())
words=json.loads((OUT/'word-alignment.json').read_text())
cue_overrides=json.loads((ROOT/'scripts/cues.json').read_text())
original=SCRIPT.read_text(encoding='utf-8-sig').splitlines()
assert len(original)==len(phrases)==522

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def tc(t):
    # Editorial display truncates microseconds; exact numeric seconds are retained.
    ms=int(round(t*1000)) if abs(t-DURATION)>.0000001 else int(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02}.{ms%1000:03}'

specs=[]
for line in (ROOT/'scripts/scenes.tsv').read_text().splitlines():
    if not line or line.startswith('#'):continue
    anchor,seq,camera,action,state=line.split('|')
    parts=anchor.split(':'); ln=int(parts[0]); wi=int(parts[1]) if len(parts)>1 else 0
    specs.append(dict(anchor=anchor,line=ln,word=wi,sequence=seq,camera=camera,action=action,end_state=state))

tokens=[]
for p in phrases:
    matches=list(re.finditer(r'[А-Яа-яЁё]+|[A-Za-z]+',p['text']))
    assert len(matches)==len(p['words']),(p['line'],len(matches),len(p['words']))
    for i,(m,w) in enumerate(zip(matches,p['words'])):
        tokens.append(dict(line=p['line'],word=i,raw_start=m.start(),raw_end=m.end(),**{k:v for k,v in w.items() if k!='line'}))
index={(w['line'],w['word']):i for i,w in enumerate(tokens)}

EGYPT={'QUARRY','QUARRY_SHAPING','EGYPT_WET_SAND','OBELISK','EGYPT_LOGISTICS','EGYPT_SOURCES','NILE','EGYPT_NETWORK'}
BRITAIN={'STONEHENGE','STONEHENGE_WATER'}
GREEK={'CLASSICAL_CRANE','CLASSICAL_TOOLKIT','GREEK_COLUMNS','LIFTING_BOSSES','JOURNEY'}
ROMAN={'ROMAN_PORT','ANIMAL_TRACTION'}
MEDIEVAL={'MEDIEVAL','SEASONAL'}
MULTI={'HOOK_EXAMPLES','PATIENCE_CULTURES','CULTURE_SCALE','SHARED_PHYSICS','FINAL_MONUMENTS'}
UNCERTAIN={'WEDGE_QUARRY','THERMAL_QUARRY','RAMP_VARIANTS','OBELISK','STONEHENGE_WATER','INCA','METHOD_UNCERTAINTY'}
def culture(seq):
    if seq in EGYPT:return 'Ancient Egypt: Nile/desert, limestone/granite, linen kilts, no later iron or classical architecture.'
    if seq in BRITAIN:return 'Prehistoric Britain: chalk grassland, rough stones, simple woven/hide clothing, no later classical architecture.'
    if seq in GREEK:return 'Classical Greek construction: chiton tunics, appropriate masonry and timber rigging, no later machinery.'
    if seq in ROMAN:return 'Roman construction/transport: tunics, classical roads or harbor masonry, period timber and fiber rigging.'
    if seq in MEDIEVAL:return 'Medieval Europe: tunics/caps, Gothic worksite or craft yard, timber scaffold and plausible period iron fittings.'
    if seq=='INCA':return 'Inca Andes: mountain landscape, woven tunics/headbands, polygonal masonry, no routine wheeled carts or European iron tools.'
    if seq in MULTI:return 'Multiple cultures in explicit separate establishing inserts; never mix costumes, crews or architectural eras.'
    if seq=='EXPERIMENT':return 'Modern manual experimental reconstruction, clearly separate from ancient scenes; no powered equipment.'
    return 'Non-specific preindustrial mechanical reconstruction; use simple tunics, earth/timber/stone and avoid attributing an uncertain method to a particular monument.'

scenes=[]; last_sequence={}
for i,s in enumerate(specs):
    begin=index[(s['line'],s['word'])]
    finish=index[(specs[i+1]['line'],specs[i+1]['word'])] if i+1<len(specs) else len(tokens)
    selected=tokens[begin:finish]; assert selected
    start=0.0 if i==0 else selected[0]['start']
    end=tokens[finish]['start'] if finish<len(tokens) else DURATION
    assert end>start
    excerpts=[]; cues=[]
    for ln in range(selected[0]['line'],selected[-1]['line']+1):
        p=phrases[ln-1]; part=[w for w in selected if w['line']==ln]
        if not part:continue
        raw_a=0 if part[0]['word']==0 else part[0]['raw_start']
        raw_b=len(p['text']) if part[-1]['word']==len(p['words'])-1 else tokens[begin+len([w for w in selected if w['line']<ln])+len(part)]['raw_start']
        excerpt=p['text'][raw_a:raw_b].strip()
        excerpts.append(excerpt)
        cues.append(dict(script_line=ln,spoken_start_seconds=part[0]['start'],spoken_end_seconds=part[-1]['end'],start_timecode=tc(part[0]['start']),end_timecode=tc(part[-1]['end']),narration_ru=excerpt,action_en=cue_overrides.get(str(ln),'Continue the authored scene action in sequence with this phrase; preserve the current load support, rigging and worker positions.'),explicit_action_override=str(ln) in cue_overrides))
    previous=last_sequence.get(s['sequence'])
    if previous:
        incoming=f"Resume {s['sequence']} from S{previous['scene_number']:03d}: {previous['end_state']}"
        if i and specs[i-1]['sequence']!=s['sequence']:incoming+=' A motivated return cut re-establishes the same geography before any new motion.'
    else:
        incoming='New established example. Show the grounded or fully supported initial state specified in the action; no physical handoff from the preceding sequence is implied.'
    scene=dict(scene_number=i+1,scene_id=f'S{i+1:03d}',start_seconds=start,end_seconds=end,start_timecode=tc(start),end_timecode=tc(end),duration_seconds=round(end-start,6),narration_ru='\n'.join(excerpts),script_lines=sorted(set(w['line'] for w in selected)),narration_spoken_start_seconds=selected[0]['start'],narration_spoken_end_seconds=selected[-1]['end'],visual_action_en=s['action'],camera=s['camera'],sequence_id=s['sequence'],historical_setting=culture(s['sequence']),heygen_clip_id=None,heygen_asset_ids=[],generation_status='not_generated_missing_authenticated_heygen_visual_generation',continuity_in=incoming,end_state=s['end_state'],continuity_out='',timed_narration_cues=cues,overlay_ru=None,alignment_method='Russian GigaAM v2 CTC forced alignment; acoustic grid 40 ms; monotonic character peak refinement',alignment_review_flags=[])
    if s['sequence'] in UNCERTAIN and previous is None:scene['overlay_ru']='Возможная реконструкция'
    weak=[w for w in selected if w['mean_log_probability'] < -2.0]
    if weak:scene['alignment_review_flags'].append('Review weak CTC words: '+', '.join(f"{w['text']} @ {tc(w['start'])}" for w in weak))
    if 379 in scene['script_lines']:scene['alignment_review_flags'].append("Supplied script includes English 'fascinates'; preserved verbatim in excerpts. Alignment-only phonetic surrogate 'фасцинейтс'; review 00:21:36.960–00:21:37.560. Do not change the master audio.")
    scenes.append(scene); last_sequence[s['sequence']]=scene

for i,s in enumerate(scenes):
    if i+1==len(scenes):s['continuity_out']='Final supported state persists through the exact master container end. No visual gap, replacement narrator, subtitle track or added speech.'
    elif scenes[i+1]['sequence_id']==s['sequence_id']:s['continuity_out']=f"Continue directly into {scenes[i+1]['scene_id']} from: {s['end_state']} Keep screen direction, anchor points, crew and support state."
    else:s['continuity_out']=f"Cut to {scenes[i+1]['scene_id']} and establish its setting. Leave this sequence at: {s['end_state']} No instantaneous transfer of this load to the next example."
    s['continuity_note']=s['continuity_in']+' NEXT: '+s['continuity_out']

# Full-source diagnostics; these are alignment checks, not a claim of video QC.
import numpy as np, soundfile as sf
audio,sr=sf.read(ROOT/'private/analysis-16k.wav',dtype='float32')
n=len(audio)//160
db=20*np.log10(np.maximum(np.sqrt((audio[:n*160].reshape(n,160)**2).mean(axis=1)),1e-7))
active=np.flatnonzero(db>-38)
greedy=json.loads((OUT/'acoustic-transcript.json').read_text())
ref=' '.join(p['normalized_alignment_text'] for p in phrases).split()
hyp=' '.join(x['text'] for x in greedy).split()
matcher=difflib.SequenceMatcher(None,ref,hyp,autojunk=False)
match_ratio=sum(x.size for x in matcher.get_matching_blocks())/len(ref)
durations=[s['duration_seconds'] for s in scenes]
meta=dict(channel='История в Палочках',topic='Как люди поднимали многотонные камни без современной техники?',language='ru',aspect_ratio='16:9',width=1920,height=1080,master_audio_original_filename='voice.mp3',script_original_filename='script.txt',brief_audio_alias='Как люди в.mp3',brief_script_alias='new_channel_02_megalith_stones_FINAL_VOICE.txt',master_audio_sha256=sha(AUDIO),script_sha256=sha(SCRIPT),master_container_duration_seconds=DURATION,master_end_timecode=tc(DURATION),brief_target_duration_seconds=1825.410,container_difference_from_brief_seconds=round(DURATION-1825.410,6),decoded_gapless_analysis_duration_seconds=len(audio)/sr,master_audio_modified=False,audio_analysis_copy='private analysis-only mono PCM at 16 kHz; not a replacement or final audio asset',scene_count=len(scenes),script_phrase_count=len(phrases),aligned_word_count=len(words),acoustic_frame_seconds=.04,scene_duration_min_seconds=min(durations),scene_duration_median_seconds=statistics.median(durations),scene_duration_max_seconds=max(durations),subtitles=False,new_voice=False,lip_sync=False,music=False,sfx_default='none',heygen_generation_available=False,blocker='No callable, authenticated HeyGen visual clip generation capability (API/MCP/SDK/browser) in this environment.',final_video_created=False,scene_manifest_complete=True,alignment_caveat='Times are acoustic model estimates on a 40 ms grid, not human-audited sample-accurate phoneme boundaries. Numeric edit boundaries are explicit; the master container end retains microseconds. Review flags are included; no audio or script correction is applied.',generated_clip_count=0)
manifest={'project':meta,'global_visual_rules':{'style':'Coherent expressive 2D stick figures: black limbs/body, light round heads, clean readable hands and restrained period-clothing shapes; tasteful bright colors; no photorealism, 3D or anime.','cuts':'Semantic clean cuts and motivated changes of scale; continuous actions retain their object state. No automatic entrances that spawn tools, people or stones.','motion':'Meaningful work, inertia, taut ropes, ground contact and correctly sequenced load transfer; no idle bouncing or unrelated mouth animation.','physics':'Visible fulcrums, supported pulleys, plausible rope paths, rotating capstan/drum tied to load motion, gradual supported lifts, low ramp travel with rollback protection.','text':'No automatic subtitles, environmental writing, watermark or fake logo. Only the explicitly listed short Russian reconstruction overlay is allowed; add it in the edit, never generate it inside a clip.','continuation':'Generate from the prior accepted final frame when a real provider supports it; keep crew, costumes, contact points, ground, direction, rope anchors, support count and action state. Provider maximum duration is unknown and must be discovered, not invented.','audio':'Use original MP3 as master at 1.0x. No cuts, new voice, pitch/tempo change or replacement track. No additional spoken dialogue. Analysis PCM is private and never the final narration.','review':'No rendered footage exists. All anatomy, rope intersection, historical architecture and motion QC remains required after real generation.'},'scenes':scenes}
(OUT/'scene-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

columns=['scene_number','scene_id','start_timecode','end_timecode','start_seconds','end_seconds','duration_seconds','narration_ru','visual_action_en','camera','sequence_id','historical_setting','heygen_clip_id','generation_status','continuity_note','end_state','overlay_ru','alignment_review_flags']
with (OUT/'scene-manifest.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=columns);writer.writeheader()
    for s in scenes:writer.writerow({k:('; '.join(s[k]) if isinstance(s[k],list) else s[k]) for k in columns})

md=['# История в Палочках — полный монтажный манифест','',f"Тема: {meta['topic']}",'',f"Мастер: **{tc(DURATION)}**, точная длительность контейнера **{DURATION:.6f} с**. Формат: 1920×1080, 16:9.",'',f"**{len(scenes)} сцен**, все 522 смысловые фразы и 3982 слова совмещены с аудио. Видео и клипы HeyGen **не созданы**: отсутствует доступная аутентифицированная функция генерации визуальных клипов HeyGen.",'','Время получено акустическим CTC-выравниванием с шагом 40 мс; это машинная оценка, а не ручная проверка каждого звука. Исходные MP3 и текст не изменены. Подробности и отмеченные слова: `alignment-report.json`. Автоматических субтитров нет.','']
for s in scenes:
    md += [f"## {s['scene_id']} · {s['start_timecode']} → {s['end_timecode']}",'',f"**Sequence:** {s['sequence_id']} · **Camera:** {s['camera']} · **Duration:** {s['duration_seconds']:.3f} s",'','**Narration (original Russian):**','',s['narration_ru'],'','**Visual/action (English):** '+s['visual_action_en'],'','**Continuity from previous:** '+s['continuity_in'],'','**End state:** '+s['end_state'],'','**Continuity to next:** '+s['continuity_out'],'','**HeyGen clip ID:** unavailable — not generated.','']
    if s['overlay_ru']:md+=['**Clean editorial overlay:** '+s['overlay_ru'],'']
    if s['alignment_review_flags']:md+=['**Alignment review:** '+'; '.join(s['alignment_review_flags']),'']
(OUT/'scene-manifest.md').write_text('\n'.join(md))

checks={
 'scene_count':len(scenes),'first_visual_at_zero':scenes[0]['start_seconds']==0,
 'last_visual_matches_original_container_end':scenes[-1]['end_seconds']==DURATION,
 'timeline_continuous':all(a['end_seconds']==b['start_seconds'] for a,b in zip(scenes,scenes[1:])),
 'all_durations_positive':all(s['duration_seconds']>0 for s in scenes),
 'script_lines_covered':sorted(set(n for s in scenes for n in s['script_lines']))==list(range(1,523)),
 'all_words_assigned_once':sum(len(tokens[index[(s['line'],s['word'])]:index[(specs[i+1]['line'],specs[i+1]['word'])] if i+1<len(specs) else len(tokens)]) for i,s in enumerate(specs))==len(words),
 'all_word_times_monotonic':all(a['end']<=b['start'] for a,b in zip(words,words[1:])),
 'all_phrase_cues_fit_visual_scene':all(s['start_seconds']<=c['spoken_start_seconds'] and c['spoken_end_seconds']<=s['end_seconds'] for s in scenes for c in s['timed_narration_cues']),
 'original_script_words_preserved':re.findall(r'[А-Яа-яЁё]+|[A-Za-z]+','\n'.join(s['narration_ru'] for s in scenes))==re.findall(r'[А-Яа-яЁё]+|[A-Za-z]+','\n'.join(original)),
 'no_fabricated_asset_ids':all(s['heygen_clip_id'] is None and not s['heygen_asset_ids'] for s in scenes),
 'audio_sha256_matches_original':'9a02ea1618ce6a0caab59a0e086e8e7f270c571d807b53c750ff0fc980b3decf'==sha(AUDIO),
 'script_sha256_matches_original':'470685d9c6bd4fdd570a67ae8f6b39ea45b844f4b789b50cc5c86469c96f659d'==sha(SCRIPT)
}
report={'checks':checks,'all_structural_checks_pass':all(v for v in checks.values() if isinstance(v,bool)),'alignment_engine':'GigaAM v2 Russian CTC int8 ONNX via official sherpa-onnx release, with kaldi-native-fbank and ctc-segmentation; real-space inter-phrase labels and monotonic character-peak refinement','model_source':'https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-ctc-giga-am-v2-russian-2025-04-19.tar.bz2','model_sha256':sha(MODEL/'model.int8.onnx'),'entire_audio_analyzed':True,'acoustic_frame_seconds':.04,'energy_analysis_frame_seconds':.01,'energy_threshold_dbfs':-38,'energy_active_first_frame_seconds':round(float(active[0])*.01,2),'energy_active_last_frame_seconds':round(float(active[-1])*.01,2),'energy_dbfs_percentiles':{str(q):round(float(np.percentile(db,q)),3) for q in [0,5,25,50,75,95,100]},'decoded_gapless_duration_seconds':len(audio)/sr,'master_container_duration_seconds':DURATION,'narration_word_range_seconds':[words[0]['start'],words[-1]['end']],'normalized_sequence_match_ratio_greedy_asr_vs_supplied_script':match_ratio,'match_ratio_definition':'SequenceMatcher matching-word count divided by normalized script word count; not word error rate, not a calibrated accuracy measure; chunk boundary token fragments contribute differences.','minimum_scene_duration_seconds':min(durations),'median_scene_duration_seconds':statistics.median(durations),'maximum_scene_duration_seconds':max(durations),'uncovered_visual_seconds':0,'hook_scene_starts_seconds':[s['start_seconds'] for s in scenes if s['start_seconds']<61.4],'alignment_flags':[{'scene_id':s['scene_id'],'start':s['start_timecode'],'flags':s['alignment_review_flags']} for s in scenes if s['alignment_review_flags']],'human_listening_review_performed':False,'generated_video_full_watch_performed':False,'limitations':['Acoustic alignment is model-derived at 40 ms resolution, with flagged weak-word/mixed-language spots; not sample-accurate human phonetic verification.','Scene physics and historical constraints have been reviewed at the manifest level only. No rendered-frame or full-video visual QC is possible before real clip generation.','MP3 container duration is 1825.410612 s; the gapless decoded analysis copy is 1825.398625 s because MP3 includes encoder delay/padding metadata. Final visual endpoint is pinned to original container duration.','A normal constant-frame-rate export may need a shortened final presentation interval/container trim to end exactly on the master; never change audio tempo to fit a frame grid.']}
(OUT/'alignment-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
assert report['all_structural_checks_pass'],checks

# Standalone review page: load the MP3 locally; it is not uploaded or embedded.
payload=json.dumps({'project':meta,'scenes':scenes},ensure_ascii=False).replace('</','<\\/')
page='''<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>История в Палочках — монтажный манифест</title><style>
:root{color-scheme:light;font-family:system-ui,sans-serif;color:#243436;background:#f5f0e5}*{box-sizing:border-box}body{margin:0}header{position:sticky;top:0;background:#fffdf7;box-shadow:0 2px 14px #2334;padding:18px 4vw;z-index:3}h1{font-size:22px;margin:0 0 8px}p{line-height:1.55}.status{color:#8b3929;font-weight:650}input[type=search]{padding:10px;width:min(100%,620px);margin:10px 0;border:1px solid #9aaba3;border-radius:6px}audio{width:min(100%,700px);vertical-align:middle}label{display:block;margin:8px 0}main{max-width:1180px;margin:auto;padding:20px}article{background:#fffdf7;padding:20px;border:2px solid transparent;border-radius:8px;margin:14px 0}article.active{border-color:#16776b}article h2{font-size:19px;margin:0 0 8px}.meta{font-family:monospace;color:#4d675f}.ru{font-size:18px;white-space:pre-line}details{margin-top:12px}summary{cursor:pointer;color:#246754}button{padding:8px 12px;border:1px solid #16776b;border-radius:4px;background:#e3f2eb;color:#234b40;cursor:pointer}.flag{color:#92361c}.hint{font-size:14px;color:#566660}.controls{display:flex;gap:12px;align-items:center;flex-wrap:wrap}#count{font-weight:600}#current{font-family:monospace}footer{padding:20px;color:#566660}
</style><header><h1>История в Палочках · полный монтажный манифест</h1><div class="status">Видео ещё не создано: нет аутентифицированной генерации визуальных клипов HeyGen.</div><div class="hint">16:9 · 1920×1080 · мастер 30:25.410612 · акустическое выравнивание 40 мс. Это страница проверки манифеста, не готовый фильм.</div><label>Локально открыть исходный MP3 для сверки тайминга: <input id="audioFile" type="file" accept="audio/*"></label><div class="controls"><audio id="audio" controls></audio><span id="current">00:00.000</span><button id="follow">Следить за текущей сценой: выкл.</button></div><div class="hint">Файл воспроизводится локально в браузере и никуда не загружается. Субтитры в финальном видео не предусмотрены.</div><input id="search" type="search" placeholder="Поиск по русскому тексту, механизму, сцене или sequence…"><span id="count"></span></header><main id="list"></main><footer>Все идентификаторы HeyGen пусты намеренно: клипы не сгенерированы. Точный конец — из метаданных исходного MP3; читаемые таймкоды округлены до миллисекунд, последний усечён. Акустические границы — машинная оценка, отмеченные слова требуют проверки.</footer><script id="data" type="application/json">__PAYLOAD__</script><script>
const data=JSON.parse(document.getElementById('data').textContent),list=document.getElementById('list'),audio=document.getElementById('audio');let follow=false,last=-1,url;
const esc=x=>String(x??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function render(){const q=document.getElementById('search').value.toLowerCase();const selected=data.scenes.filter(s=>JSON.stringify(s).toLowerCase().includes(q));document.getElementById('count').textContent=` ${selected.length} / ${data.scenes.length} сцен`;list.innerHTML=selected.map(s=>`<article id="${s.scene_id}" data-n="${s.scene_number}"><h2>${s.scene_id} · ${s.start_timecode} → ${s.end_timecode}</h2><div class="meta">${esc(s.sequence_id)} · ${s.duration_seconds.toFixed(3)} s · ${esc(s.camera)}</div><p class="ru" lang="ru">${esc(s.narration_ru)}</p><p lang="en">${esc(s.visual_action_en)}</p><button data-seek="${s.start_seconds}">▶ Слушать с начала сцены</button>${s.alignment_review_flags.map(f=>`<p class="flag">${esc(f)}</p>`).join('')}<details><summary>Continuity / timed phrase cues / setting</summary><p>${esc(s.historical_setting)}</p><p><b>IN:</b> ${esc(s.continuity_in)}</p><p><b>END:</b> ${esc(s.end_state)}</p><p><b>NEXT:</b> ${esc(s.continuity_out)}</p>${s.overlay_ru?`<p>Overlay: ${esc(s.overlay_ru)}</p>`:''}${s.timed_narration_cues.map(c=>`<p><span class="meta">${c.start_timecode}–${c.end_timecode}</span><br>${esc(c.narration_ru)}<br><span lang="en">${esc(c.action_en)}</span></p>`).join('')}<p>HeyGen clip ID: null — not generated.</p></details></article>`).join('');}
document.getElementById('search').addEventListener('input',render);list.addEventListener('click',e=>{const b=e.target.closest('[data-seek]');if(!b)return;if(!audio.src){alert('Сначала откройте исходный MP3 локально.');return;}audio.currentTime=Number(b.dataset.seek);audio.play().catch(()=>{});});document.getElementById('audioFile').addEventListener('change',e=>{if(url)URL.revokeObjectURL(url);if(e.target.files[0]){url=URL.createObjectURL(e.target.files[0]);audio.src=url;}});document.getElementById('follow').addEventListener('click',e=>{follow=!follow;e.target.textContent='Следить за текущей сценой: '+(follow?'вкл.':'выкл.');});audio.addEventListener('timeupdate',()=>{const t=audio.currentTime;document.getElementById('current').textContent=`${String(Math.floor(t/60)).padStart(2,'0')}:${(t%60).toFixed(3).padStart(6,'0')}`;const s=data.scenes.find(s=>t>=s.start_seconds&&t<s.end_seconds);if(s&&s.scene_number!==last){document.querySelector('article.active')?.classList.remove('active');const el=document.getElementById(s.scene_id);el?.classList.add('active');if(follow)el?.scrollIntoView({block:'center',behavior:'smooth'});last=s.scene_number;}});render();
</script></html>'''
(OUT/'review-manifest.html').write_text(page.replace('__PAYLOAD__',payload))
print(json.dumps({'scene_count':len(scenes),'duration':DURATION,'durations_min_median_max':[min(durations),statistics.median(durations),max(durations)],'checks':checks,'flagged_scenes':len(report['alignment_flags'])},indent=2))
