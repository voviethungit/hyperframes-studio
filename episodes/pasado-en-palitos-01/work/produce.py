import subprocess,json,os,time,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;os.chdir(ROOT)
def run(args,log):
 print('RUN',args,flush=True)
 with open(log,'w') as f:subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,check=True)
while not Path('work/asr.json').exists():time.sleep(5)
run(['python','work/plan.py'],'work/plan-full.log')
run(['python','work/sfx.py'],'work/sfx.log')
run(['node','node_modules/@remotion/cli/remotion-cli.js','bundle','src/index.jsx','work/bundle'],'work/bundle.log')
p=json.load(open('output/scene_plan.json'));total=math.ceil(p['duration']*30);Path('work/render-chunks').mkdir(exist_ok=True);manifest={'source_sha256':hashlib.sha256(Path('cuidado_ab.mp3').read_bytes()).hexdigest(),'frames':total,'chunks':[]}
for a in range(0,total,3600):
 b=min(total,a+3600)-1;dest=f'work/render-chunks/{a:06}-{b:06}.mp4'
 if not Path(dest+'.done').exists():
  run(['node','node_modules/@remotion/cli/remotion-cli.js','render','work/bundle','Episode',dest,f'--frames={a}-{b}','--codec=h264','--crf=22','--muted','--concurrency=1','--gl=angle'],f'work/render-{a:06}.log')
  Path(dest+'.done').write_text('complete')
 manifest['chunks'].append({'start_frame':a,'end_frame':b,'file':dest,'status':'complete'})
 Path('output/cache_manifest.json').write_text(json.dumps(manifest,indent=2))
Path('work/concat.txt').write_text(''.join("file '"+str(ROOT/c['file'])+"'\n" for c in manifest['chunks']))
run(['ffmpeg','-v','warning','-f','concat','-safe','0','-i','work/concat.txt','-i','cuidado_ab.mp3','-i','work/sfx.wav','-filter_complex','[1:a]volume=0.85[v];[v][2:a]amix=inputs=2:duration=first:normalize=0[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(p['duration']),'-movflags','+faststart','-y','output/pasado_en_palitos_01.mp4'],'work/mux.log')
run(['python','work/qa.py'],'work/qa.log')
Path('work/production-complete').write_text('done')
