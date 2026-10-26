from pathlib import Path
s=Path('src/index.jsx').read_text().replace('useCurrentFrame()','0')
s=s[:s.index('registerRoot(()=>')]
s=s.replace("<Audio src={staticFile('cuidado_ab.mp3')} volume={.85}/>",'')
s+='\nimport {renderToStaticMarkup} from "react-dom/server";\nexport function frameSVG(frame){const text=renderToStaticMarkup(<Scene frame={frame}/>);return text.slice(text.indexOf("<svg"),text.indexOf("</svg>")+6).replace("<svg ","<svg xmlns=\\\"http://www.w3.org/2000/svg\\\" ");}\n'
Path('src/native.jsx').write_text(s)
