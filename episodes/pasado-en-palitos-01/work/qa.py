import subprocess,json,hashlib,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
p='output/pasado_en_palitos_01.mp4'
def probe(p):return json.loads(subprocess.check_output(['ffprobe','-v','quiet','-show_streams','-show_format','-of','json',p]))
v=probe(p);src=probe('cuidado_ab.mp3');T=float(src['format']['duration']);vs=next(s for s in v['streams'] if s['codec_type']=='video');au=next(s for s in v['streams'] if s['codec_type']=='audio')
report={'source':src,'output':v,'checks':{'resolution':vs['width']==1920 and vs['height']==1080,'fps':vs['avg_frame_rate']=='30/1','codec':vs['codec_name']=='h264' and au['codec_name']=='aac','duration_difference':float(v['format']['duration'])-T,'expected_frames':math.ceil(T*30),'reported_frames':int(vs.get('nb_frames',0))},'frame_samples':[]}
plan=json.load(open('output/scene_plan.json'));marks=plan['milestones'];times=[]
for i,(st,typ) in enumerate(marks):
 en=marks[i+1][0] if i+1<len(marks) else T
 for t in [min(en-.1,st+.1),(st+en)/2,max(st,en-.15)]:times.append((t,typ))
Path('work/qa-frames').mkdir(exist_ok=True)
thumbs=[]
for i,(t,typ) in enumerate(times):
 dest=f'work/qa-frames/{i:03}.jpg'
 subprocess.run(['ffmpeg','-v','error','-ss',str(max(0,t)),'-i',p,'-frames:v','1','-vf','scale=480:270','-y',dest],check=True)
 im=Image.open(dest).convert('RGB');ar=np.array(im);report['frame_samples'].append({'time':t,'section':typ,'mean':float(ar.mean()),'std':float(ar.std()),'black':bool(ar.mean()<2)})
 canvas=Image.new('RGB',(480,300),'#202b32');canvas.paste(im,(0,0));ImageDraw.Draw(canvas).text((10,278),f'{t:07.2f}s  {typ}',fill='white');thumbs.append(canvas)
sheet=Image.new('RGB',(480*4,300*math.ceil(len(thumbs)/4)),'#202b32')
for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*480,(i//4)*300))
sheet.save('output/contact_sheet.jpg',quality=87)
def pcm(p):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',p,'-vn','-ar','16000','-ac','1','-f','f32le','-']),dtype=np.float32)
x=pcm('cuidado_ab.mp3');y=pcm(p);N=min(len(x),len(y));gain=float(np.dot(x[:N],y[:N])/np.dot(x[:N],x[:N]));corr=float(np.corrcoef(x[:N],y[:N])[0,1]);report['audio_compare']={'sample_rate':16000,'source_samples':len(x),'output_samples':len(y),'gain':gain,'correlation':corr,'method':'sample-by-sample decoded correlation; AAC loss expected','no_stretch_or_edit_in_pipeline':True}
json.dump(report,open('output/qa_report.json','w'),ensure_ascii=False,indent=2)
print(json.dumps({'checks':report['checks'],'audio_compare':report['audio_compare']},indent=2))
