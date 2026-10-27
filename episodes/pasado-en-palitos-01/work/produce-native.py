exec(open('work/produce.py').read().split("while not Path('work/asr.json').exists()")[0])
while not Path('work/asr.json').exists():time.sleep(5)
run(['python','work/plan.py'],'work/plan-full.log')
run(['python','work/subtitles.py'],'work/subtitles.log')
run(['python','work/sfx.py'],'work/sfx.log')
run(['python','work/build-native.py'],'work/build-native-source.log')
run(['node_modules/.bin/esbuild','src/native.jsx','--bundle','--platform=node','--external:react','--external:react-dom/server','--outfile=work/native.cjs'],'work/build-native.log')
p=json.load(open('output/scene_plan.json'));total=math.ceil(p['duration']*30);Path('work/native-chunks').mkdir(exist_ok=True);manifest={'source_sha256':hashlib.sha256(Path('cuidado_ab.mp3').read_bytes()).hexdigest(),'frames':total,'animation_poses_per_second':15,'output_fps':30,'backend':'Remotion React SVG scenes, React SSR, resvg native raster, FFmpeg','chunks':[]}
config_sha=hashlib.sha256(Path('src/index.jsx').read_bytes()+Path('work/render-layered.cjs').read_bytes()+Path('output/scene_plan.json').read_bytes()).hexdigest()
manifest['render_config_sha256']=config_sha
config_file=Path('work/native-chunks/config.sha256')
if not config_file.exists() or config_file.read_text()!=config_sha:
 for marker in Path('work/native-chunks').glob('*.done'):marker.unlink()
 config_file.write_text(config_sha)
for a in range(0,total,3600):
 b=min(total,a+3600);dest=f'work/native-chunks/{a:06}-{b:06}.mp4'
 if not Path(dest+'.done').exists():
  run(['node','work/render-layered.cjs',str(a),str(b),dest],f'work/native-{a:06}.log')
  Path(dest+'.done').write_text('complete')
 manifest['chunks'].append({'start_frame':a,'end_frame_exclusive':b,'file':dest,'status':'complete'})
 Path('output/cache_manifest.json').write_text(json.dumps(manifest,indent=2))
Path('work/concat.txt').write_text(''.join("file '"+str(ROOT/c['file'])+"'\n" for c in manifest['chunks']))
run(['ffmpeg','-v','warning','-f','concat','-safe','0','-i','work/concat.txt','-i','cuidado_ab.mp3','-i','work/sfx.wav','-filter_complex','[1:a]volume=0.85[v];[v][2:a]amix=inputs=2:duration=first:normalize=0[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(p['duration']),'-movflags','+faststart','-y','output/pasado_en_palitos_01.mp4'],'work/mux.log')
run(['python','work/qa.py'],'work/qa.log')
Path('work/production-complete').write_text('done')
