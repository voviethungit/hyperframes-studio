from pathlib import Path
import subprocess,os,wave
import numpy as np
ROOT=Path(__file__).resolve().parents[2];os.chdir(ROOT)
subprocess.run(['node','work/style-v2/render.cjs'],check=True)
sr=44100;T=2480/30;mix=np.zeros(round(T*sr),np.float32);t=np.arange(int(.35*sr))/sr;rng=np.random.default_rng(1290);noise=rng.standard_normal(len(t));z=(.65*np.sin(2*np.pi*53*t)+.35*np.convolve(noise,np.ones(30)/30,'same'))*np.exp(-t*7)*.025;st=round(9.32*sr);mix[st:st+len(z)]+=z
with wave.open('work/style-v2/preview_sfx.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((mix*32767).astype('<i2').tobytes())
subprocess.run(['ffmpeg','-v','warning','-i','work/style-v2/video.mp4','-i','cuidado_ab.mp3','-i','work/style-v2/preview_sfx.wav','-filter_complex','[1:a]volume=0.85[v];[v][2:a]amix=inputs=2:duration=first:normalize=0[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','192k','-t',str(T),'-movflags','+faststart','-y','output/style_v2/preview_style_v2.mp4'],check=True)
