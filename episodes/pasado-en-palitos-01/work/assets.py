from pathlib import Path
import json
head='''<g id="head"><circle cy="-211" r="58" fill="#fffdf4"/><path id="hair" d="M-56 -220Q-65 -277 -16 -272Q32 -284 57 -245L57 -220L23 -249L-3 -240L-15 -254L-39 -226Z" fill="#202b32"/><g id="eyes"><ellipse cx="-20" cy="-210" rx="8" ry="12" fill="#202b32"/><ellipse cx="20" cy="-210" rx="8" ry="12" fill="#202b32"/></g><path id="brows" d="M-31 -233L-12 -235M12 -235L31 -233"/><path id="mouth" d="M-18 -184Q0 -166 18 -184" fill="none"/></g>'''
rig=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="-120 -300 250 330"><g stroke="#202b32" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><path id="torso" d="M0 -155V-75"/><path id="left-arm" d="M0 -140L-38 -108L-48 -70" fill="none"/><path id="right-arm" d="M0 -140L38 -108L48 -70" fill="none"/><path id="left-leg" d="M0 -75L-33 0"/><path id="right-leg" d="M0 -75L33 0"/>{head}<g id="scarf" fill="#f4bd32"><path d="M-18 -158L24 -158L38 -140L-12 -140Z"/><path d="M19 -145Q48 -133 72 -160L65 -118L20 -129Z"/></g></g></svg>'''
Path('output/assets/hero-01.svg').write_text(rig)
items=['FRENTE','PERFIL IZQUIERDO','PERFIL DERECHO','ESPALDA','ASUSTADO','SORPRENDIDO','AGOTADO','ENFADADO','CONFIADO','ALIVIADO','CONFUNDIDO','CORRER','CAER','CARGAR','SEÑALAR','CORTAR']
sheet='<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1600" viewBox="0 0 1920 1600"><rect width="1920" height="1600" fill="#f7efd9"/>'
for i,label in enumerate(items):
 x=(i%4)*480;y=(i//4)*400
 body=rig[rig.index('<g'):rig.rindex('</svg>')]
 if i==3:body=body.replace('id="eyes"','id="eyes" visibility="hidden"').replace('id="mouth"','id="mouth" visibility="hidden"').replace('id="brows"','id="brows" visibility="hidden"')
 if i in [1,2]:body=body.replace('rx="8"','rx="5"');body=f'<g transform="scale({-.62 if i==1 else .62} 1)">{body}</g>'
 if i in [4,5]:body=body.replace('M-18 -184Q0 -166 18 -184','M-10 -185Q-20 -155 10 -172Q25 -194 -10 -185')
 if i==6:body=body.replace('ry="12"','ry="3"').replace('M-18 -184Q0 -166 18 -184','M-15 -175Q0 -185 15 -175')
 if i==7:body=body.replace('M-31 -233L-12 -235M12 -235L31 -233','M-32 -244L-12 -232M12 -232L32 -244').replace('M-18 -184Q0 -166 18 -184','M-18 -174Q0 -190 18 -174')
 if i==9:body=body.replace('ry="12"','ry="3"')
 if i==10:body=body.replace('M-31 -233L-12 -235M12 -235L31 -233','M-31 -241L-12 -244M12 -232L31 -232').replace('M-18 -184Q0 -166 18 -184','M-12 -180Q0 -186 12 -180')
 if i==11:body=body.replace('M0 -75L-33 0','M0 -75L-60 -50L-90 0').replace('M0 -75L33 0','M0 -75L60 -25L90 -60')
 if i==12:body=f'<g transform="rotate(-65 0 -120)">{body}</g>'
 if i==13:body=body.replace('M0 -140L38 -108L48 -70','M0 -140L55 -170L65 -220').replace('M0 -140L-38 -108L-48 -70','M0 -140L-55 -170L-65 -220')
 if i==14:body=body.replace('M0 -140L38 -108L48 -70','M0 -140L55 -170L105 -170')
 if i==15:body=body.replace('M0 -140L38 -108L48 -70','M0 -140L55 -110L100 -145')
 sheet+=f'<g transform="translate({x+240} {y+320}) scale(.9)">{body}</g><text x="{x+240}" y="{y+370}" text-anchor="middle" font-size="25" font-family="sans-serif" fill="#202b32">{label}</text>'
sheet+='</svg>';Path('output/assets/character_reference.svg').write_text(sheet)
json.dump({'hero_id':'hero-01','joints':{'neck':[0,-155],'hip':[0,-75],'head':[0,-211]},'layer_ids':['torso','left-arm','right-arm','left-leg','right-leg','head','hair','eyes','brows','mouth','scarf'],'wardrobe':'golden scarf, black side-part 70/30'},open('output/assets/rig.json','w'),indent=2)
