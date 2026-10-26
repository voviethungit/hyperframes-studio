process.env.NODE_ENV='production';
const fs=require('fs'),path=require('path'),{spawn}=require('child_process'),{once}=require('events');
const {Resvg}=require('@resvg/resvg-js'),{createCanvas,ImageData}=require('@napi-rs/canvas');
const A=require('./art.cjs');const {P,E,G,T,svg}=A;
const ROOT=path.resolve(__dirname,'../..'),DEST=path.join(ROOT,'output/style_v2');fs.mkdirSync(DEST,{recursive:true});
const font=path.join(__dirname,'assets/PatrickHand-Regular.ttf');
const opts={font:{loadSystemFonts:false,fontFiles:[font],defaultFontFamily:'Patrick Hand',sansSerifFamily:'Patrick Hand'}};
const cache=new Map();
function picture(body,key=body){if(cache.has(key)){let v=cache.get(key);cache.delete(key);cache.set(key,v);return v}let r=new Resvg(body.startsWith('<svg')?body:svg(body),opts);let b=r.getBBox();if(!b||b.width<1||b.height<1)return null;r.cropByBBox(b);let pic=r.render(),c=createCanvas(pic.width,pic.height);c.getContext('2d').putImageData(new ImageData(new Uint8ClampedArray(pic.pixels),pic.width,pic.height),0,0);let im={c,x:b.x,y:b.y,w:b.width,h:b.height};cache.set(key,im);if(cache.size>95)cache.delete(cache.keys().next().value);return im}
const canvas=createCanvas(1920,1080),ctx=canvas.getContext('2d');
const backgrounds={barn:picture(A.barn(),'bg-barn'),village:picture(A.village(),'bg-village')};
function paint(body,x=0,y=0,scale=1,rot=0,key=body){let im=picture(body,key);if(!im)return;ctx.save();ctx.translate(x,y);ctx.rotate(rot*Math.PI/180);ctx.scale(scale,scale);ctx.drawImage(im.c,im.x,im.y,im.w,im.h);ctx.restore()}
function bg(name){let im=backgrounds[name];ctx.drawImage(im.c,im.x,im.y,im.w,im.h)}
const clamp=x=>Math.max(0,Math.min(1,x)),ease=x=>{x=clamp(x);return x*x*(3-2*x)};
function camera(z=1,x=960,y=540){x=Math.max(960/z,Math.min(1920-960/z,x));y=Math.max(540/z,Math.min(1080-540/z,y));ctx.save();ctx.translate(960,540);ctx.scale(z,z);ctx.translate(-x,-y)}
function shadow(x,y,rx=100){ctx.save();ctx.fillStyle='rgba(78,61,42,.12)';ctx.beginPath();ctx.ellipse(x,y,rx,14,0,0,Math.PI*2);ctx.fill();ctx.restore()}
function actor(x,y,pose='stand',emotion='confused',phase=0,gaze=0,scale=1,rot=0,extra={}){paint(A.hero({pose,emotion,phase,gaze,...extra}),x,y,scale,rot)}
function cow(t){paint(A.cowBody(),1300,960);let lift=t<8.87?200:t<9.32?200*(1-ease((t-8.87)/.45)):0;paint(A.cowLeg(lift),1300,960)}
function dust(t){const p=clamp((t-9.32)/.65);if(t<9.32||p>=1)return;ctx.save();ctx.globalAlpha=1-p;for(let i=0;i<13;i++){let a=(-Math.PI+i*Math.PI/12),rr=30+p*(80+(i%3)*24);let x=1490+Math.cos(a)*rr,y=958+Math.sin(a)*rr*.6;paint(P('M-8 0q7 -8 16 -1q-4 9 -16 1Z',i%2?'#c5a377':'#edd29b',1.4,'#9d7b51'),x,y)}ctx.restore()}
function white(){ctx.fillStyle='#fffdfa';ctx.fillRect(0,0,1920,1080)}
function underline(x,y,w,color='#b9d9d3'){ctx.save();ctx.strokeStyle=color;ctx.lineWidth=25;ctx.lineCap='round';ctx.beginPath();ctx.moveTo(x,y);ctx.quadraticCurveTo(x+w*.5,y-8,x+w,y-2);ctx.stroke();ctx.restore()}
function questionCards(){white();const items=[['¿MI CAMA?',A.bed()],['¿MI TELÉFONO?',A.phone()],['¿MI CASA?',A.house(-150,150,1)]];items.forEach(([label,body],i)=>{let x=360+i*600;paint(body,x,560,i===2?.9:1);paint(T(label,0,0,51),x-170,830);paint(T('?',0,0,76,'#a05b4e'),x+140,320)});}
function strawCards(){white();paint(A.hay(0,0,.95),360,650);paint(P('M-180 0Q-100 -70 -30 -32Q70 -96 159 -25Q226 17 131 49Q15 76 -140 38Z','#ad8f68',3.7)+P('M-92 7q51 -19 101 0m30 8q39 -18 68 -2','none',2,'#83694d'),965,670);paint(A.cowBody()+A.cowLeg(0),1550,790,.40);paint(T('PAJA',0,0,55),300,840);paint(T('BARRO',0,0,55),885,840);paint(T('ANIMALES',0,0,55),1430,840)}
function historyCard(t){white();paint(A.hourglass(),395,565,1.10);paint(P('M580 435Q905 216 1283 386M1255 351L1292 386L1243 391','none',5),0,0);underline(796,503,660);paint(T('INGLATERRA',0,0,107),800,487);if(t>=68.82){paint(T('1290',0,0,181),980,736);paint(P('M944 767Q1160 790 1370 762','none',4),0,0)}paint(A.castle(0,0,.56),1590,768);}
function scarcity(t){white();actor(455,860,'shrug','confused',0,1,1.20);if(t<72.94){paint(P('M-58 -40Q-116 57 -69 115Q0 149 71 111Q108 45 60 -39Z','#b99b74',4)+P('M-53 -38Q0 -58 58 -38L43 -74L-39 -75Z','#d5bc91',3)+P('M-57 -35Q-6 -14 60 -38M-34 -54L35 -52','none',3,'#765c43'),1170,590,1.15);paint(T('SIN DINERO',0,0,78),950,840);paint(P('M1052 384L1289 719','none',8,'#b94c43'))}else{paint(T('¿Y AHORA?',0,0,96),1010,520);paint(P('M1045 580q145 48 306 -4','none',3.5),0,0);paint(T('No conoces a nadie.',0,0,52),990,690)}}
function phoneCard(){white();actor(450,865,'shrug','confused',0,1,1.15);paint(A.phone(),1200,552,1.35);paint(P('M1075 330L1324 784','none',10,'#b94c43'));paint(T('SIN TELÉFONO',0,0,73),990,907)}
function challenge(t){white();if(t>=79.9){underline(735,414,594,'#efd78e');paint(T('24 HORAS',0,0,137),739,400);paint(T('¿SOBREVIVIRÍAS?',0,0,75),748,570);paint(A.hourglass(),1530,698,.75)}else{paint(T('TENEMOS UN PROBLEMA…',0,0,88),660,470)}actor(405,880,'shrug','scared',0,1,1.20)}
function frame(t){white();
 if(t<18.36){let z=1,x=960,y=540;if(t<5.88){let p=ease((t-1.3)/3.7);z=2-p*.8;x=1450-p*180;y=845-p*105}else if(t>=9.03&&t<13.32){z=1.9;x=1490;y=875}else if(t>=13.32){z=1.65;x=650;y=785}camera(z,x,y);bg('barn');cow(t);
 if(t<5.88){shadow(1320,981,190);actor(1180,890,'stand','scared',0,1,1,90,{blink:t<.20})}
 else if(t<8.98){let p=ease((t-5.88)/2.85),xx=1365-800*p;shadow(xx,991,100);actor(xx,890-42*Math.sin(p*Math.PI),'stand','scared',0,1,1,90-360*p,{roll:true})}
 else if(t<13.32){shadow(529,981,155);actor(380,890,'stand','scared',0,1,1,90)}
 else{let p=ease((t-13.32)/1.1);shadow(650,976,82);actor(650,1165-205*p,'heart','scared',t,1);if(t>14.8&&t<17.9){let a=(t-14.8)*5;paint(P('M0 10C-35 -19 -47 -52 -22 -60Q-3 -63 1 -46Q19 -66 36 -54Q60 -35 0 10Z','#ba6053',3),785,745,1+Math.max(0,Math.sin(a))*.10)}}dust(t);ctx.restore();if(t<.9)paint(T('¡CUIDADO!',0,0,92,'#9a473d'),87,148);if(t>=9.32&&t<10.02)paint(T('¡PUM!',0,0,111,'#664a35'),960,266);
 }else if(t<21.2)questionCards();
 else if(t<24.96)strawCards();
 else if(t<29.8){camera(1.55,650,760);bg('barn');actor(650,960,'nose','exhausted',t,1);for(let i=0;i<3;i++)paint(P(`M0 0q${12+Math.sin(t*3+i)*5} -26 0 -49t0 -45`,'none',3,'#9b9b6c'),780+i*38,841-i*18);ctx.restore()}
 else if(t<34.24){let p=ease((t-29.8)/3.6),xx=1070-p*930;camera(1.1,740,660);bg('barn');shadow(xx,977,85);actor(xx,960,'run','scared',t,-1,.93);ctx.restore()}
 else if(t<40){let p=ease((t-35.6)/1.3);camera(1+p*.25,960-45*p,540+130*p);bg('village');actor(602,960,'stand',t<35.7?'shock':'confused',0,t<37?1:-1,1.04);let xx=1390-(t-34.24)*73;actor(xx,914,'run','relieved',t,-1,.73,0,{farmer:true});paint(P('M0 0L30 -91','none',7,'#826648')+P('M30 -91Q115 -149 71 -190Q169 -144 30 -91Z','#b6b7ad',2.7),xx-27,807,.7);ctx.restore()}
 else if(t<42){white();paint(A.castle(0,0,1.57),1000,734);paint(P('M450 515Q593 385 728 443M694 409L737 442L687 453','none',4.5));paint(T('AL FONDO…',0,0,67),339,698);}
 else if(t<66.38){let progress=ease((t-42)/3.72),cartX=1815-progress*840,farmerX=cartX+312;let z=t>=48.36&&t<57.2?1.28:t>=63.6?1.75:1;let fx=t>=63.6?602:t>=48.36&&t<57.2?1000:960;camera(z,fx,t>=63.6?760:540);bg('village');paint(A.cart(),cartX,960,.91);actor(farmerX,953,t<45.72?'push':t<57.2?'point':'shrug',t<57.2?'relieved':'confused',t,-1,.94,-8,{farmer:true});actor(602,960,t<45.72?'stand':t<48.36?'point':t<63.6?'shrug':'stand',t>=63.6?'shock':'confused',0,1,1.04);if(t>=48.36&&t<57.2){paint(P('M-150 0Q-197 -47 -137 -86Q-63 -115 77 -91Q164 -80 151 -21Q145 31 38 30L-7 67L-6 30Q-112 40 -150 0Z','#fffaf0',3.6)+P('M-106 -48q29 -27 57 -1t55 -2t58 1M-95 -13q20 -13 46 -1t49 1','none',3.2),farmerX-30,575,.9);paint(T('?',0,0,85),683,542)}if(t>=57.2&&t<63.6){paint(T('?',0,0,72),695,560);paint(T('…',0,0,80),farmerX-24,572)}ctx.restore()}
 else if(t<71.7)historyCard(t);
 else if(t<74.42)scarcity(t);
 else if(t<78.22)phoneCard();
 else challenge(t);
}
async function main(){let still=process.argv.indexOf('--stills')>=0;if(still){let times=[0.6,4.5,7.4,9.55,14.8,19.1,26.2,35.5,43.2,50,69.9,81];for(let i=0;i<times.length;i++){frame(times[i]);fs.writeFileSync(path.join(DEST,`frame-${String(i).padStart(2,'0')}.png`),canvas.toBuffer('image/png'))}console.log('Saved',times.length,'style frames');return}
 let n=2480,dest=path.join(ROOT,'work/style-v2/video.mp4');const enc=spawn('ffmpeg',['-v','warning','-f','rawvideo','-pixel_format','rgba','-video_size','1920x1080','-framerate','30','-i','pipe:0','-an','-c:v','libx264','-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-threads','2','-y',dest],{stdio:['pipe','inherit','inherit']});let begin=Date.now();for(let f=0;f<n;f++){frame(f/30);let data=ctx.getImageData(0,0,1920,1080).data;if(!enc.stdin.write(data))await once(enc.stdin,'drain');if(f%180===0)console.log(f,n,((Date.now()-begin)/1000).toFixed(1),'s')}enc.stdin.end();let [code]=await once(enc,'close');if(code)throw Error('FFmpeg '+code);console.log('Render finished')}
main().catch(e=>{console.error(e);process.exit(1)});
