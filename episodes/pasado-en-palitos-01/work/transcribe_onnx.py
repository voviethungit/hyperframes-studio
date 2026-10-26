import sherpa_onnx, numpy as np, subprocess,json,re,hashlib
from pathlib import Path
source_sha=hashlib.sha256(Path('cuidado_ab.mp3').read_bytes()).hexdigest()
manifest=Path('work/asr-source.sha256')
if manifest.exists() and manifest.read_text()!=source_sha:
 raise RuntimeError('Audio source changed; archive old ASR cache before transcribing a new source.')
manifest.write_text(source_sha)
m='.cache/reference-asr/sherpa-onnx-whisper-base/'
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=m+'base-encoder.int8.onnx',decoder=m+'base-decoder.int8.onnx',tokens=m+'base-tokens.txt',language='es',task='transcribe',num_threads=2,enable_token_timestamps=False,enable_segment_timestamps=True)
audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i','cuidado_ab.mp3','-f','f32le','-ar','16000','-ac','1','-']),dtype=np.float32)
# Speech boundary selection from measured short-window energy; cap chunks below Whisper context.
step=320; energies=np.array([np.sqrt(np.mean(audio[i:i+step]**2)) for i in range(0,len(audio),step)])
bounds=[0];pos=0
while pos+26<len(audio)/16000:
 lo=int((pos+18)/.02);hi=int((pos+27)/.02); idx=lo+np.argmin(np.convolve(energies[lo:hi],np.ones(12)/12,'same'))
 pos=idx*.02;bounds.append(pos)
bounds.append(len(audio)/16000)
out=[]
for i,(st,en) in enumerate(zip(bounds,bounds[1:])):
 cache=Path(f'work/asr-chunk-{i:03}.json')
 if cache.exists():out.append(json.loads(cache.read_text()));continue
 s=r.create_stream();s.accept_waveform(16000,audio[int(st*16000):int(en*16000)]);r.decode_stream(s);res=s.result
 d={'start':st,'end':en,'text':res.text,'words':[],'confidence':None,'boundary_method':'measured waveform minimum in 18–27 s window; segment-level ASR; no word alignment'}
 print(i,round(en,2),res.text,flush=True)
 try:d['tokens']=res.tokens;d['token_timestamps']=res.timestamps;d['raw_result']=str(res)
 except Exception:pass
 cache.write_text(json.dumps(d,ensure_ascii=False));out.append(d)
 json.dump({'segments':out,'complete':False},open('work/asr-progress.json','w'),ensure_ascii=False,indent=2)
json.dump({'segments':out,'complete':True,'language':'es'},open('work/asr.json','w'),ensure_ascii=False,indent=2)
