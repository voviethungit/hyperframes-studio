from pathlib import Path
import zipfile,json,hashlib
files=[Path('package.json'),Path('package-lock.json'),Path('tsconfig.json'),Path('remotion.config.ts'),Path('requirements.txt'),Path('cuidado_ab.mp3'),Path('guion_01_es.txt')]
files+=list(Path('src').glob('*'))
files+=[p for p in Path('work').glob('*') if p.suffix in ['.py','.cjs'] or p.name.startswith('asr-chunk-') or p.name in ['probe.json','asr.json','audio-analysis.log','asr-source.sha256']]
files+=[p for p in Path('output').rglob('*') if p.is_file() and p.suffix not in ['.mp4','.zip'] and p.name!='source_manifest.json']
models=Path('.cache/reference-asr/sherpa-onnx-whisper-base');files += [models/f for f in ['base-encoder.int8.onnx','base-decoder.int8.onnx','base-tokens.txt']]
manifest=[]
with zipfile.ZipFile('output/reproducible_project.zip','w',zipfile.ZIP_DEFLATED,compresslevel=3) as z:
 for p in files:
  if not p.exists():continue
  z.write(p,str(p));manifest.append({'path':str(p),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
 z.writestr('output/source_manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2))
Path('output/source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
