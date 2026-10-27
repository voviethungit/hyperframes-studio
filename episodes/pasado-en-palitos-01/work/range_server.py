from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent.parent
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_HEAD(self):self.serve(False)
 def do_GET(self):self.serve(True)
 def serve(self,body):
  allowed={'/work/playback.html':('work/playback.html','text/html'),'/output/pasado_en_palitos_01.mp4':('output/pasado_en_palitos_01.mp4','video/mp4')}
  if self.path.split('?')[0] not in allowed:self.send_error(404);return
  rel,mime=allowed[self.path.split('?')[0]];p=ROOT/rel;n=p.stat().st_size;start=0;end=n-1;rg=self.headers.get('Range');m=re.match(r'bytes=(\d+)-(\d*)',rg or '')
  if m:start=int(m[1]);end=min(n-1,int(m[2]) if m[2] else n-1)
  if start>=n:self.send_error(416);return
  self.send_response(206 if m else 200);self.send_header('Content-Type',mime);self.send_header('Accept-Ranges','bytes');self.send_header('Content-Length',str(end-start+1));self.send_header('Cache-Control','no-store')
  if m:self.send_header('Content-Range',f'bytes {start}-{end}/{n}')
  self.end_headers()
  if body:
   try:
    with p.open('rb') as f:
     f.seek(start);remaining=end-start+1
     while remaining:
      data=f.read(min(262144,remaining))
      if not data:break
      self.wfile.write(data);remaining-=len(data)
   except (BrokenPipeError,ConnectionResetError):pass
ThreadingHTTPServer(('127.0.0.1',8765),Handler).serve_forever()
