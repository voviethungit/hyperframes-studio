import json, re, time, hashlib, os, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf
import kaldi_native_fbank as knf
import onnxruntime as ort
from ctc_segmentation import CtcSegmentationParameters, prepare_text, ctc_segmentation, determine_utterance_segments

ROOT = Path(os.environ.get('MEGALITH_PROJECT_DIR',Path(__file__).resolve().parents[1]))
MODEL = Path(os.environ.get('MEGALITH_MODEL_DIR',ROOT/'models/sherpa-onnx-nemo-ctc-giga-am-v2-russian-2025-04-19'))
SCRIPT = Path(os.environ.get('MEGALITH_SCRIPT',ROOT/'private/source-script.txt'))
SOURCE_AUDIO = Path(os.environ.get('MEGALITH_AUDIO',ROOT/'private/voice.mp3'))
(ROOT/'private').mkdir(exist_ok=True,parents=True)
(ROOT/'deliverables').mkdir(exist_ok=True,parents=True)
if not (ROOT/'private/analysis-16k.wav').exists():
    subprocess.run(['ffmpeg','-v','error','-i',str(SOURCE_AUDIO),'-ar','16000','-ac','1','-c:a','pcm_s16le',str(ROOT/'private/analysis-16k.wav')],check=True)
audio, sr = sf.read(ROOT/'private/analysis-16k.wav', dtype='float32')
assert sr == 16000
lines = SCRIPT.read_text(encoding='utf-8-sig').splitlines()
lines = [x.strip() for x in lines if x.strip()]
char_list = [''] * 34
for line in (MODEL/'tokens.txt').read_text().splitlines():
    fields = line.split()
    if len(fields) == 1: char_list[int(fields[0])] = ' '
    else: char_list[int(fields[1])] = fields[0]

opts = knf.FbankOptions()
opts.frame_opts.dither=0
opts.frame_opts.remove_dc_offset=False
opts.frame_opts.preemph_coeff=0
opts.frame_opts.window_type='hann'
opts.frame_opts.round_to_power_of_two=False
opts.mel_opts.low_freq=0
opts.mel_opts.high_freq=8000
opts.mel_opts.num_bins=64

if not (ROOT/'private/log_probs.npy').exists():
    print('Computing acoustic features',len(audio)/sr,flush=True)
    fb=knf.OnlineFbank(opts); fb.accept_waveform(sr,audio); fb.input_finished()
    features=np.array([fb.get_frame(i) for i in range(fb.num_frames_ready)],dtype=np.float32)
    so=ort.SessionOptions();so.intra_op_num_threads=4;so.inter_op_num_threads=1
    sess=ort.InferenceSession(str(MODEL/'model.int8.onnx'),sess_options=so,providers=['CPUExecutionProvider'])
    outputs=[]; greedy=[]; t0=time.monotonic()
    for core in range(0,len(features),2000):
        a=max(0,core-200); b=min(len(features),core+2200)
        x=features[a:b].T[None]
        y=sess.run(None,{'features':x,'feature_lengths':np.array([b-a],np.int64)})[0][0]
        first=(core-a)//4; n=min(500,(len(features)-core+3)//4)
        y=y[first:first+n]
        outputs.append(y)
        prev=-1; text=''
        for v in np.argmax(y,axis=1):
            if v!=33 and v!=prev:text+=char_list[v]
            prev=v
        greedy.append({'start':core*.01,'end':min(core+2000,len(features))*.01,'text':text})
        print(f'ASR {min(core+2000,len(features))*.01:.1f}/{len(audio)/sr:.1f}s | elapsed {time.monotonic()-t0:.1f}s | {text[:90]}',flush=True)
    lp=np.concatenate(outputs)
    np.save(ROOT/'private/log_probs.npy',lp)
    (ROOT/'deliverables/acoustic-transcript.json').write_text(json.dumps(greedy,ensure_ascii=False,indent=2))
else: lp=np.load(ROOT/'private/log_probs.npy')

# Normalize only the alignment input; all delivered excerpts retain exact script wording.
normalized=[]
for line in lines:
    s=line.lower().replace('ё','е').replace('fascinates','фасцинейтс')
    s=re.sub('[^а-я ]',' ',s)
    normalized.append(' '.join(s.split()))
cfg=CtcSegmentationParameters(char_list=char_list,blank=33,index_duration=.04,min_window_size=8000)
gt,begins=prepare_text(cfg,normalized)
# GigaAM emits a real space label (0). Keep it between script lines as well;
# treating those separators as acoustic blank would pull first vowels into pauses.
gt[np.array(begins),0]=0
print('Aligning',len(gt),'characters',len(lp),'acoustic frames',flush=True)
timings,probs,states=ctc_segmentation(cfg,lp,gt)
segments=determine_utterance_segments(cfg,begins,probs,timings,normalized)
np.savez(ROOT/'private/ctc-alignment.npz',timings=timings,char_probs=probs,ground_truth=gt,begins=begins)
# CTC segmentation reports state entry, which can precede its acoustic peak.
# Refine each character within its own state interval, retaining monotonic order.
peak_times=timings.copy()
for j in range(2,len(gt)-1):
    token=int(gt[j,0])
    if token<0: continue
    lo=max(0,int(round(timings[j]/.04)))
    hi=min(len(lp),max(lo+1,int(round(timings[j+1]/.04))))
    if hi>lo: peak_times[j]=(lo+int(np.argmax(lp[lo:hi,token])))*.04
aligned=[]; words=[]
for i,(line,norm,(start,end,score)) in enumerate(zip(lines,normalized,segments)):
    # Character transition times, not interpolation from text length.
    cursor=begins[i]+1
    local=[]
    for m in re.finditer(r'\S+',norm):
        ids=list(range(cursor+m.start(),cursor+m.end()))
        t1=float(peak_times[ids[0]])
        t2=float(peak_times[ids[-1]]+.04)
        ps=[float(lp[min(int(round(peak_times[j]/.04)),len(lp)-1),gt[j,0]]) for j in ids]
        w={'line':i+1,'text':m.group(),'start':round(t1,3),'end':round(t2,3),'mean_log_probability':round(float(np.mean(ps)),4)}
        words.append(w);local.append(w)
    aligned.append({'line':i+1,'text':line,'normalized_alignment_text':norm,'start':round(local[0]['start'],3),'end':round(local[-1]['end'],3),'ctc_segment_start':round(float(start),3),'ctc_segment_end':round(float(end),3),'ctc_confidence':round(float(score),4),'words':local})
(ROOT/'deliverables/phrase-alignment.json').write_text(json.dumps(aligned,ensure_ascii=False,indent=2))
(ROOT/'deliverables/word-alignment.json').write_text(json.dumps(words,ensure_ascii=False,indent=2))
print('DONE',len(aligned),'phrases',len(words),'words',flush=True)
for a in aligned:
    print(f"{a['line']:03d} {a['start']:8.2f}-{a['end']:8.2f} conf={a['ctc_confidence']:6.2f} {a['text']}")
