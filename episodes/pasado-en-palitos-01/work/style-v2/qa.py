from pathlib import Path
import subprocess,json,hashlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[2]
p=ROOT/'output/style_v2/preview_style_v2.mp4'
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]));v=next(x for x in probe['streams'] if x['codec_type']=='video');a=next(x for x in probe['streams'] if x['codec_type']=='audio')
q={'duration':float(probe['format']['duration']),'frames':int(v['nb_frames']),'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],'video_codec':v['codec_name'],'audio_codec':a['codec_name'],'full_episode_replaced':False,'source_excerpt':[0,2480/30]}
assert q['frames']==2480 and q['width']==1920 and q['height']==1080 and q['fps']=='30/1'
log=subprocess.run(['ffmpeg','-v','info','-nostats','-threads','2','-i',str(p),'-an','-vf','blackdetect=d=0.1:pix_th=0.02','-f','null','-'],capture_output=True,text=True)
q['full_decode_exit_code']=log.returncode;q['black_detected']='black_start:' in log.stderr
(ROOT/'work/style-v2/decode.log').write_text(log.stderr)
def pcm(f):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(f),'-t',str(2480/30),'-vn','-ar','16000','-ac','1','-f','f32le','-']),np.float32)
x=pcm(ROOT/'cuidado_ab.mp3');y=pcm(p);N=min(len(x),len(y));q['voice_correlation']=float(np.corrcoef(x[:N],y[:N])[0,1]);q['voice_gain']=float(np.dot(x[:N],y[:N])/np.dot(x[:N],x[:N]));q['source_sha256']=hashlib.sha256((ROOT/'cuidado_ab.mp3').read_bytes()).hexdigest()
times=[.6,4.5,7.4,9.55,14.8,19.1,26.2,35.5,43.2,50,69.9,81];sheet=Image.new('RGB',(1920,930),'#f8f0dd')
for i,t in enumerate(times):
 dest=ROOT/f'work/style-v2/qa-{i:02}.jpg';subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-frames:v','1','-vf','scale=480:270','-y',str(dest)],check=True);xx=i%4*480;yy=i//4*310;sheet.paste(Image.open(dest),(xx,yy));ImageDraw.Draw(sheet).text((xx+13,yy+283),f'{t:.2f}s',fill='#302820')
sheet.save(ROOT/'output/style_v2/contact_sheet.jpg',quality=90)
(ROOT/'output/style_v2/qa_report.json').write_text(json.dumps(q,ensure_ascii=False,indent=2));print(json.dumps(q,ensure_ascii=False,indent=2))
