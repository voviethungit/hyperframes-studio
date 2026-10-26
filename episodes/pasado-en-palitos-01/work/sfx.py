import numpy as np,json,wave
p=json.load(open('output/scene_plan.json'));sr=44100;N=int(np.ceil(p['duration']*sr));mix=np.zeros(N,dtype=np.float32);rng=np.random.default_rng(1290);events=[]
for s in p['scenes']:
 tx=s['audio_text'].lower();kind=None
 if 'pum' in tx:kind='hoof'
 elif 'trueno' in tx or 'treno' in tx:kind='thunder'
 elif 'plof' in tx or 'plove' in tx:kind='mud'
 elif 'carro sale' in tx:kind='wood'
 if kind:
  d={'hoof':.35,'thunder':2.1,'mud':.5,'wood':.8}[kind];t=np.arange(int(d*sr))/sr;noise=rng.standard_normal(len(t));f={'hoof':53,'thunder':35,'mud':83,'wood':180}[kind]
  z=(.65*np.sin(2*np.pi*f*t)+.35*np.convolve(noise,np.ones(30)/30,'same'))*np.exp(-t*(7 if kind!='thunder' else 2))*.025
  st=int(s['start']*sr);en=min(N,st+len(z));mix[st:en]+=z[:en-st];events.append({'time':s['start'],'type':kind,'peak_dbfs':float(20*np.log10(max(abs(z))))})
with wave.open('work/sfx.wav','wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.clip(mix,-1,1)*32767).astype('<i2').tobytes())
json.dump({'source':'procedural synthesis; no voices','events':events},open('output/sfx_manifest.json','w'),indent=2)
