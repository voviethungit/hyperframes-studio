from pathlib import Path
import json,textwrap
p=json.load(open('output/audio_alignment.json'));s=p['segments'];cues=[];adjust=[]
for i,x in enumerate(s):
 end=min(x['end'],s[i+1]['start'] if i+1<len(s) else p['duration'])
 if end<x['end']:adjust.append({'cue':i+1,'raw_end':x['end'],'display_end':end,'reason':'cap at next measured ASR segment onset'})
 cues.append((x['start'],max(end,x['start']+.001),'\n'.join(textwrap.wrap(x['text'].strip(),52,break_long_words=False,break_on_hyphens=False))))
def ts(t,sep):
 ms=round(t*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);ss,ms=divmod(ms,1000);return f'{h:02}:{m:02}:{ss:02}{sep}{ms:03}'
Path('output/subtitles_es.srt').write_text('\n\n'.join(f'{i+1}\n{ts(st,",")} --> {ts(en,",")}\n{tx}' for i,(st,en,tx) in enumerate(cues))+'\n')
Path('output/subtitles_es.vtt').write_text('WEBVTT\n\n'+'\n\n'.join(f'{ts(st,".")} --> {ts(en,".")}\n{tx}' for st,en,tx in cues)+'\n')
json.dump({'confidence':'ASR phrases; manual correction pending','cue_count':len(cues),'overlap_adjustments':adjust},open('output/subtitle_qa.json','w'),ensure_ascii=False,indent=2)
