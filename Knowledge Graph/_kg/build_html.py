#!/usr/bin/env python3
"""Pass 3: render a self-contained interactive HTML graph from graph.json.
Acceler-branded, light theme, skim-friendly. Logo embedded as base64."""
import json, os, base64
OUT = "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Knowledge Graph/_kg"
LOGO = "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Live Session-Deck-Builder/acceler_logo.png"
graph = json.load(open(os.path.join(OUT, "graph.json")))
DATA = json.dumps(graph, ensure_ascii=False)
LOGO_B64 = ""
if os.path.exists(LOGO):
    LOGO_B64 = "data:image/png;base64," + base64.b64encode(open(LOGO, "rb").read()).decode()

HTML = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Acceler · Pre-Sales Knowledge Graph</title>
<style>
:root{
  --navy:#27B4E6; --navy2:#9FD9F2; --cyan:#27B4E6; --teal:#5BC4D2;
  --ink:#E8EDF9; --mut:#9AA6C8; --line:#243161; --line2:#1B2750;
  --bg:#0B1228; --panel:#121B3A; --soft:#1A2750; --cyansoft:#13343f;
  --client:#3FA9F5; --program:#9A8CFF; --tool:#43C8DE; --topic:#F0A64E;
  --instructor:#EF7BA6; --doctype:#8893A8;
  --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;
}
*{box-sizing:border-box}
html,body{margin:0;height:100%;font-family:var(--font);background:var(--bg);color:var(--ink);overflow:hidden}
#app{display:flex;flex-direction:column;height:100vh}

/* ---- top bar ---- */
#top{display:flex;align-items:center;gap:18px;padding:11px 20px;background:var(--panel);border-bottom:1px solid var(--line);box-shadow:0 2px 10px rgba(0,0,0,.25);z-index:20}
#top .logo{height:24px;display:block;background:#fff;padding:7px 13px;border-radius:9px;box-shadow:0 2px 8px rgba(0,0,0,.2)}
#top .ttl{display:flex;flex-direction:column;line-height:1.2;border-left:1px solid var(--line);padding-left:16px}
#top .ttl b{font-size:14.5px;font-weight:800;letter-spacing:.2px}
#top .ttl span{font-size:11px;color:var(--mut);margin-top:2px;letter-spacing:.04em}
#stats{display:flex;gap:9px;margin-left:auto;flex-wrap:wrap}
.stat{background:var(--soft);border:1px solid var(--line);border-radius:10px;padding:5px 12px;text-align:center;min-width:64px}
.stat b{display:block;font-size:16px;font-weight:800;color:var(--navy)}
.stat span{font-size:9.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--mut)}

#main{display:flex;flex:1;min-height:0}
#graphwrap{position:relative;flex:1;background:
  radial-gradient(circle at 32% 18%, #16204a 0%, var(--bg) 72%)}
canvas{display:block;cursor:grab}canvas:active{cursor:grabbing}
#tip{position:absolute;pointer-events:none;background:#020615;color:#fff;font-size:11.5px;
  padding:5px 9px;border-radius:7px;opacity:0;transition:opacity .1s;white-space:nowrap;z-index:30;box-shadow:0 6px 18px rgba(0,0,0,.45);border:1px solid var(--line)}
#ctrls{position:absolute;left:16px;bottom:14px;display:flex;gap:7px}
.cbtn{width:34px;height:34px;border-radius:9px;border:1px solid var(--line);background:var(--panel);
  color:var(--cyan);font-size:17px;font-weight:700;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.3)}
.cbtn:hover{border-color:var(--cyan);background:var(--soft)}
#hint{position:absolute;right:16px;bottom:14px;font-size:11px;color:var(--mut);background:rgba(10,16,40,.8);padding:6px 11px;border-radius:8px;border:1px solid var(--line)}

/* ---- side ---- */
#side{width:400px;min-width:400px;background:var(--panel);border-left:1px solid var(--line);display:flex;flex-direction:column;height:100%}
#search{margin:14px 16px 8px;position:relative}
#search input{width:100%;background:var(--bg);border:1.5px solid var(--line);border-radius:10px;padding:10px 12px 10px 34px;font-size:13px;outline:none;color:var(--ink)}
#search input:focus{border-color:var(--cyan)}
#search .mag{position:absolute;left:11px;top:9px;color:var(--mut);font-size:14px}
#results{position:absolute;top:42px;left:0;right:0;background:var(--panel);border:1px solid var(--line);border-radius:10px;box-shadow:0 14px 34px rgba(0,0,0,.5);max-height:300px;overflow:auto;z-index:40;display:none}
#results .r{padding:8px 12px;font-size:12.5px;cursor:pointer;display:flex;align-items:center;gap:8px;border-bottom:1px solid var(--line2)}
#results .r:hover{background:var(--soft)}
#results .r .k{font-size:9px;text-transform:uppercase;letter-spacing:.05em;color:#fff;padding:2px 6px;border-radius:5px;flex-shrink:0}

.filters{display:flex;flex-wrap:wrap;gap:7px;padding:4px 16px 12px;border-bottom:1px solid var(--line)}
.flt{display:flex;align-items:center;gap:7px;font-size:11.5px;font-weight:600;color:var(--ink);cursor:pointer;user-select:none;
  background:var(--soft);border:1px solid var(--line);border-radius:20px;padding:5px 12px 5px 9px;transition:background .12s,border-color .12s}
.flt:hover{border-color:var(--cyan)}
.flt .dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.flt.off{background:transparent;border-color:var(--line2);color:var(--mut)}
.flt.off .dot{background:transparent!important;box-shadow:inset 0 0 0 2px var(--mut)}
.flt .dot.client{background:var(--client)}.flt .dot.program{background:var(--program)}
.flt .dot.tool{background:var(--tool)}.flt .dot.topic{background:var(--topic)}
.flt .dot.instructor{background:var(--instructor)}.flt .dot.doctype{background:var(--doctype)}

#panel{flex:1;overflow:auto;padding:14px 18px 40px}
.empty{color:var(--mut);font-size:13px;line-height:1.7}
.empty h3{color:var(--ink);font-size:14px;margin:0 0 8px}
.empty .row{display:flex;gap:8px;align-items:flex-start;margin:7px 0}
.empty .row .d{width:9px;height:9px;border-radius:50%;margin-top:4px;flex-shrink:0}

.nkind{font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;font-weight:800;color:var(--cyan)}
.ntitle{font-size:19px;font-weight:800;margin:4px 0 3px;line-height:1.25;color:var(--navy)}
.sub{font-size:12px;color:var(--mut);line-height:1.5}
.linkedin{display:inline-flex;align-items:center;gap:5px;margin-top:9px;color:#fff;background:#0A66C2;text-decoration:none;font-size:11.5px;font-weight:700;padding:5px 11px;border-radius:7px}
.sec{font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--mut);font-weight:800;margin:18px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--line)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{background:var(--soft);border:1px solid var(--line);border-radius:20px;padding:4px 10px;font-size:11.5px;color:var(--navy2);font-weight:600}
.chip.tool{background:var(--cyansoft);border-color:#1f5560;color:#9ee6f3}
.chip.topic{background:#33270f;border-color:#5c4a23;color:#f0c285;cursor:pointer}
.chip.topic:hover{background:#43330f}
.chip.inst{background:#3a1f2c;border-color:#7a3a55;color:#f6c9da}

/* pricing bands */
.pband{display:flex;gap:9px;align-items:baseline;margin:7px 0;font-size:12px}
.pband .lbl{font-size:9.5px;text-transform:uppercase;letter-spacing:.06em;font-weight:800;color:var(--mut);width:64px;flex-shrink:0;padding-top:2px}
.pband .vals{display:flex;flex-wrap:wrap;gap:5px}
.pval{background:#12321f;border:1px solid #225437;color:#7fe0a4;border-radius:7px;padding:3px 9px;font-weight:700;font-size:11.5px;font-variant-numeric:tabular-nums}
.pval.deal{background:#33270d;border-color:#5e4a1c;color:#f0c074}
.pval.margin{background:#241f47;border-color:#3f377a;color:#bcb0f5}

.grp{font-size:12px;font-weight:800;color:var(--navy2);margin:14px 0 3px;display:flex;justify-content:space-between}
.grp .c{color:var(--mut);font-weight:600;font-size:11px}
.frow{display:flex;justify-content:space-between;gap:8px;padding:7px 0;border-bottom:1px solid var(--line2);cursor:pointer}
.frow:hover{background:var(--soft);margin:0 -8px;padding:7px 8px;border-radius:6px}
.fname{font-size:12.5px;color:var(--ink);line-height:1.35}
.fmeta{font-size:11px;color:var(--mut);margin-top:3px;line-height:1.4}
.pill{display:inline-block;background:var(--bg);border:1px solid var(--line);border-radius:5px;padding:1px 6px;font-size:10px;color:var(--mut);margin-right:4px;margin-top:3px}
.backbar{display:flex;align-items:center;gap:6px;cursor:pointer;color:var(--navy2);font-size:12px;font-weight:700;padding:8px 11px;margin-bottom:12px;background:var(--soft);border:1px solid var(--line);border-radius:8px}
.backbar:hover{border-color:var(--cyan);color:var(--cyan)}
.open{color:var(--cyan);text-decoration:none;font-size:12px;font-weight:700}
.open:hover{text-decoration:underline}
.path{font-size:10.5px;color:var(--mut);word-break:break-all;background:var(--bg);padding:7px 9px;border-radius:7px;border:1px solid var(--line2);margin-top:5px}
::-webkit-scrollbar{width:9px}::-webkit-scrollbar-thumb{background:#2A3866;border-radius:6px}::-webkit-scrollbar-track{background:transparent}
</style></head><body>
<div id="app">
 <div id="top">
   <img class="logo" src="__LOGO__" alt="Acceler"/>
   <div class="ttl"><b>Pre-Sales Knowledge Graph</b><span>Programs · Accounts · Tools · Topics · Instructors</span></div>
   <div id="stats"></div>
 </div>
 <div id="main">
   <div id="graphwrap">
     <canvas id="cv"></canvas>
     <div id="tip"></div>
     <div id="ctrls">
       <button class="cbtn" id="zin" title="Zoom in">+</button>
       <button class="cbtn" id="zout" title="Zoom out">−</button>
       <button class="cbtn" id="reset" title="Reset view">⤾</button>
     </div>
     <div id="hint">drag node · scroll = zoom · click = details · drag canvas = pan</div>
   </div>
   <div id="side">
     <div id="search">
       <span class="mag">⌕</span>
       <input id="q" placeholder="Search accounts, programs, instructors, files…" autocomplete="off"/>
       <div id="results"></div>
     </div>
     <div class="filters" id="filters"></div>
     <div id="panel"></div>
   </div>
 </div>
</div>
<script>
const G = __DATA__;
const files = G.nodes.filter(n=>n.type==='file');
const instructors = G.nodes.filter(n=>n.type==='instructor');
const back = G.nodes.filter(n=>n.type!=='file');
const byId = {}; G.nodes.forEach(n=>byId[n.id]=n);
const filesByClient={}, filesByProgram={}, filesByTool={}, filesByTopic={}, instByTopic={}, instByClient={};
files.forEach(f=>{
  (filesByClient[f.client]=filesByClient[f.client]||[]).push(f);
  if(f.program)(filesByProgram[f.program]=filesByProgram[f.program]||[]).push(f);
  (f.tools||[]).forEach(t=>(filesByTool[t]=filesByTool[t]||[]).push(f));
  (f.topics||[]).forEach(t=>(filesByTopic[t]=filesByTopic[t]||[]).push(f));
});
instructors.forEach(p=>{
  (p.topics||[]).forEach(t=>(instByTopic[t]=instByTopic[t]||[]).push(p));
  (p.clients||[]).forEach(c=>(instByClient[c]=instByClient[c]||[]).push(p));
});
const bedges = G.edges.filter(e=>byId[e.source]&&byId[e.target]&&byId[e.source].type!=='file'&&byId[e.target].type!=='file');

const M=G.meta;
document.getElementById('stats').innerHTML=[
  ['files',M.files],['accounts',M.clients],['programs',M.programs],
  ['instructors',M.instructors||0],['topics',M.topics||0],['tools',M.tools]
].map(([l,v])=>`<div class="stat"><b>${v}</b><span>${l}</span></div>`).join('');

const COL={client:'#1B2A6B',program:'#7C6CFF',tool:'#16A6C9',doctype:'#8893A8',topic:'#E8913A',instructor:'#E0598B'};
const show={client:true,program:true,tool:false,doctype:false,topic:true,instructor:false};
const filters=document.getElementById('filters');
[['client','Accounts'],['program','Programs'],['topic','Topics'],['instructor','Instructors'],['tool','Tools'],['doctype','Doc types']].forEach(([k,lab])=>{
  const el=document.createElement('div');el.className='flt'+(show[k]?'':' off');
  el.innerHTML=`<span class="dot ${k}"></span>${lab}`;
  el.onclick=()=>{show[k]=!show[k];el.classList.toggle('off');layoutInit();};
  filters.appendChild(el);
});

const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,DPR=window.devicePixelRatio||1;
function resize(){const r=cv.parentElement.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
window.addEventListener('resize',resize);resize();

let view={x:W/2,y:H/2,k:0.85};
let N=[],E=[],sel=null,hover=null,q='',drag=null,panning=false,last=null,alpha=1;
function active(n){return show[n.type];}
function layoutInit(){
  N=back.filter(active);
  const idset=new Set(N.map(n=>n.id));
  E=bedges.filter(e=>idset.has(e.source)&&idset.has(e.target));
  N.forEach((n,i)=>{ if(n.x===undefined){const a=i*2.399;const r=40+Math.sqrt(i)*46;n.x=Math.cos(a)*r;n.y=Math.sin(a)*r;n.vx=0;n.vy=0;} });
  alpha=1;
}
function rad(n){
  if(n.type==='client')return 7+Math.min(16,Math.sqrt(n.count));
  if(n.type==='program')return 9+Math.min(15,Math.sqrt(n.count));
  if(n.type==='topic')return 9+Math.min(15,Math.sqrt(n.count));
  if(n.type==='instructor')return 4+Math.min(6,Math.sqrt(n.count));
  return 5+Math.min(9,Math.sqrt(n.count));}
layoutInit();

function tick(){
  for(let i=0;i<N.length;i++){const a=N[i];
    for(let j=i+1;j<N.length;j++){const b=N[j];
      let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+0.01;
      if(d2<90000){let f=440/d2;a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f;}
    }
    a.vx-=a.x*0.0016;a.vy-=a.y*0.0016;
  }
  E.forEach(e=>{const a=byId[e.source],b=byId[e.target];if(a.x===undefined||b.x===undefined)return;
    let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)||1;
    let target=72+(e.weight?Math.min(40,e.weight*3):0);
    let f=(d-target)*0.02*(e.rel==='engages'?1.4:1);
    let fx=dx/d*f,fy=dy/d*f;a.vx+=fx;a.vy+=fy;b.vx-=fx;b.vy-=fy;});
  N.forEach(n=>{if(n===drag)return;n.x+=n.vx*alpha;n.y+=n.vy*alpha;n.vx*=0.86;n.vy*=0.86;});
  if(alpha>0.02)alpha*=0.994;
}
function toScreen(n){return{x:view.x+n.x*view.k,y:view.y+n.y*view.k};}
function neighbor(n){return sel&&(n===sel||E.some(e=>(e.source===sel.id&&e.target===n.id)||(e.target===sel.id&&e.source===n.id)));}
function draw(){
  ctx.clearRect(0,0,W,H);
  E.forEach(e=>{const a=byId[e.source],b=byId[e.target];const pa=toScreen(a),pb=toScreen(b);
    const hot=sel&&(e.source===sel.id||e.target===sel.id);
    ctx.strokeStyle=hot?'rgba(39,180,230,.5)':'rgba(120,135,180,.12)';
    ctx.lineWidth=hot?1.7:1;
    ctx.beginPath();ctx.moveTo(pa.x,pa.y);ctx.lineTo(pb.x,pb.y);ctx.stroke();});
  N.forEach(n=>{const p=toScreen(n);const r=rad(n)*Math.max(.6,Math.min(1.4,view.k));
    const dim=sel&&!neighbor(n);
    ctx.globalAlpha=dim?0.22:1;
    ctx.beginPath();ctx.arc(p.x,p.y,r,0,7);ctx.fillStyle=COL[n.type];ctx.fill();
    if(n===sel){ctx.lineWidth=3;ctx.strokeStyle='#fff';ctx.stroke();ctx.lineWidth=2;ctx.strokeStyle=COL[n.type];ctx.stroke();}
    else if(n===hover){ctx.lineWidth=2;ctx.strokeStyle='#fff';ctx.stroke();}
    if(view.k>0.75||(n.type!=='tool'&&n.type!=='instructor')||n===hover||n===sel){
      ctx.globalAlpha=dim?0.3:1;ctx.fillStyle=n.type==='client'?'#eaf3ff':'#b9c4e6';
      ctx.font=(n.type==='client'||n.type==='program'?'700 ':'600 ')+Math.round(11.5*Math.min(1.2,Math.max(.85,view.k)))+'px '+getComputedStyle(document.body).fontFamily;
      let lab=n.label.length>28?n.label.slice(0,27)+'…':n.label;
      ctx.fillText(lab,p.x+r+4,p.y+4);}
    ctx.globalAlpha=1;});
}
function loop(){tick();draw();requestAnimationFrame(loop);}loop();

function pick(mx,my){let best=null,bd=18;
  for(const n of N){const p=toScreen(n);const d=Math.hypot(p.x-mx,p.y-my);if(d<Math.max(bd,rad(n)*view.k+6)&&d<bd+rad(n)){if(d<bd){bd=d;best=n;}}}
  return best;}
const tip=document.getElementById('tip');
cv.addEventListener('mousedown',e=>{const m=rel(e);const n=pick(m.x,m.y);if(n){drag=n;nav(n);}else{panning=true;}last=m;});
window.addEventListener('mousemove',e=>{const m=rel(e);
  if(drag){drag.x=(m.x-view.x)/view.k;drag.y=(m.y-view.y)/view.k;alpha=Math.max(alpha,.4);tip.style.opacity=0;}
  else if(panning){view.x+=m.x-last.x;view.y+=m.y-last.y;}
  else{hover=pick(m.x,m.y);cv.style.cursor=hover?'pointer':'grab';
    if(hover){tip.textContent=hover.label;tip.style.left=(m.x+14)+'px';tip.style.top=(m.y+12)+'px';tip.style.opacity=1;}
    else tip.style.opacity=0;}
  last=m;});
window.addEventListener('mouseup',()=>{drag=null;panning=false;});
cv.addEventListener('wheel',e=>{e.preventDefault();const m=rel(e);const f=Math.exp(-e.deltaY*0.0012);
  view.x=m.x-(m.x-view.x)*f;view.y=m.y-(m.y-view.y)*f;view.k*=f;view.k=Math.max(.15,Math.min(4,view.k));},{passive:false});
function rel(e){const r=cv.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top};}
function zoomBy(f){view.x=W/2-(W/2-view.x)*f;view.y=H/2-(H/2-view.y)*f;view.k=Math.max(.15,Math.min(4,view.k*f));}
document.getElementById('zin').onclick=()=>zoomBy(1.25);
document.getElementById('zout').onclick=()=>zoomBy(.8);
document.getElementById('reset').onclick=()=>{view={x:W/2,y:H/2,k:0.85};};

// ---- search with dropdown ----
const qbox=document.getElementById('q'),results=document.getElementById('results');
const searchable=[...back,...instructors,...files];
qbox.addEventListener('input',e=>{
  q=e.target.value.toLowerCase().trim();
  if(!q){results.style.display='none';return;}
  const hits=searchable.filter(n=>n.label.toLowerCase().includes(q)).slice(0,40)
    .sort((a,b)=>a.label.toLowerCase().indexOf(q)-b.label.toLowerCase().indexOf(q));
  if(!hits.length){results.style.display='none';return;}
  results.innerHTML=hits.map(n=>{const t=n.type;const c=COL[t]||'#888';
    return `<div class="r" data-id="${esc(n.id)}"><span class="k" style="background:${c}">${t.slice(0,4)}</span>${esc(n.label)}</div>`;}).join('');
  results.style.display='block';
  results.querySelectorAll('.r').forEach(r=>r.onclick=()=>{results.style.display='none';qbox.value='';nav(byId[r.dataset.id]);});
});
document.addEventListener('click',e=>{if(!document.getElementById('search').contains(e.target))results.style.display='none';});

// ---- side panel ----
const panel=document.getElementById('panel');
function esc(s){return (s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function priceBands(b){
  if(!b)return '';
  let h='';
  if(b.rates&&b.rates.length)h+=`<div class="pband"><span class="lbl">Rates</span><div class="vals">${b.rates.map(v=>`<span class="pval">${esc(v)}</span>`).join('')}</div></div>`;
  if(b.deals&&b.deals.length)h+=`<div class="pband"><span class="lbl">Deal size</span><div class="vals">${b.deals.map(v=>`<span class="pval deal">${esc(v)}</span>`).join('')}</div></div>`;
  if(b.margin)h+=`<div class="pband"><span class="lbl">Margin</span><div class="vals"><span class="pval margin">${esc(b.margin)}</span></div></div>`;
  return h;
}
function mergeBands(fs){
  const out={rates:[],deals:[],margin:null};
  fs.forEach(f=>{const b=f.price_bands;if(!b)return;
    (b.rates||[]).forEach(v=>out.rates.includes(v)||out.rates.push(v));
    (b.deals||[]).forEach(v=>out.deals.includes(v)||out.deals.push(v));
    if(b.margin)out.margin=b.margin;});
  out.rates=out.rates.slice(0,10);out.deals=out.deals.slice(0,8);
  return (out.rates.length||out.deals.length||out.margin)?out:null;
}
function fileRow(f){
  const meta=[f.program,f.version,f.duration,f.cohort?f.cohort+' pax':null,f.ext.replace('.','')].filter(Boolean).map(x=>`<span class="pill">${esc(x)}</span>`).join('');
  return `<div class="frow" data-id="${f.id}"><div><div class="fname">${esc(f.label)}</div><div class="fmeta">${meta}</div></div></div>`;
}
function bindRows(){panel.querySelectorAll('.frow[data-id]').forEach(r=>r.onclick=()=>nav(byId['F:'+r.dataset.id]||byId[r.dataset.id]));}
function chip(arr,cls){return (arr||[]).map(x=>`<span class="chip ${cls}">${esc(x)}</span>`).join('');}
function instRow(p){const tp=(p.topics||[]).slice(0,4).map(t=>`<span class="pill">${esc(t)}</span>`).join('');
  return `<div class="frow" data-iid="${esc(p.id)}"><div><div class="fname">${esc(p.label)}</div>`+
    (p.role?`<div class="fmeta">${esc((p.role||'').slice(0,95))}</div>`:'')+
    `<div>${tp}</div></div></div>`;}
function bindInst(){panel.querySelectorAll('.frow[data-iid]').forEach(r=>r.onclick=()=>nav(byId[r.dataset.iid]));}

let navHist=[],curNode=null;
function nav(node){if(!node)return;if(curNode&&curNode.id!==node.id)navHist.push(curNode);
  curNode=node;sel=node;renderPanel(node);injectBack();panel.scrollTop=0;}
function goBack(){if(!navHist.length)return;const prev=navHist.pop();curNode=prev;sel=prev;renderPanel(prev);injectBack();panel.scrollTop=0;}
function injectBack(){if(!navHist.length)return;const prev=navHist[navHist.length-1];
  const lab=prev.label.length>34?prev.label.slice(0,33)+'…':prev.label;
  const bar=document.createElement('div');bar.className='backbar';bar.textContent='← Back to '+lab;bar.onclick=goBack;
  panel.insertBefore(bar,panel.firstChild);}

function renderPanel(n){
  sel=n.type==='file'?sel:n;
  if(n.type==='client'){
    const fs=(filesByClient[n.label]||[]).slice().sort((a,b)=>(a.program||'~').localeCompare(b.program||'~'));
    const progs={};fs.forEach(f=>{const p=f.program||'Unsorted';(progs[p]=progs[p]||[]).push(f);});
    const tools=[...new Set(fs.flatMap(f=>f.tools||[]))];
    const topics=[...new Set(fs.flatMap(f=>f.topics||[]))];
    const team=instByClient[n.label]||[];
    const bands=mergeBands(fs);
    let h=`<div class="nkind">Account</div><div class="ntitle">${esc(n.label)}</div>
      <div class="sub">${fs.length} files · ${Object.keys(progs).length} programs</div>`;
    if(bands){h+=`<div class="sec">Pricing seen</div>${priceBands(bands)}`;}
    if(topics.length)h+=`<div class="sec">Topics covered</div><div class="chips">${chip(topics,'topic')}</div>`;
    if(tools.length)h+=`<div class="sec">Tools / Tech</div><div class="chips">${chip(tools,'tool')}</div>`;
    if(team.length)h+=`<div class="sec">Instructors proposed (${team.length})</div>`+team.slice(0,30).map(instRow).join('');
    h+=`<div class="sec">Files by program</div>`;
    Object.keys(progs).sort().forEach(p=>{h+=`<div class="grp">${esc(p)}<span class="c">${progs[p].length}</span></div>`+progs[p].map(fileRow).join('');});
    panel.innerHTML=h;bindRows();bindInst();bindTopicChips();
  } else if(n.type==='program'){
    const fs=filesByProgram[n.label]||[];
    const clients={};fs.forEach(f=>{(clients[f.client]=clients[f.client]||[]).push(f);});
    const tools=[...new Set(fs.flatMap(f=>f.tools||[]))];
    const bands=mergeBands(fs);
    let h=`<div class="nkind">Program</div><div class="ntitle">${esc(n.label)}</div>
      <div class="sub">${fs.length} files · ${Object.keys(clients).length} accounts</div>`;
    if(bands){h+=`<div class="sec">Pricing seen</div>${priceBands(bands)}`;}
    if(tools.length)h+=`<div class="sec">Tools / Tech</div><div class="chips">${chip(tools,'tool')}</div>`;
    h+=`<div class="sec">Accounts running this</div>`;
    Object.keys(clients).sort((a,b)=>clients[b].length-clients[a].length).forEach(c=>{h+=`<div class="grp">${esc(c)}<span class="c">${clients[c].length}</span></div>`+clients[c].map(fileRow).join('');});
    panel.innerHTML=h;bindRows();
  } else if(n.type==='tool'){
    const fs=filesByTool[n.label]||[];
    const clients={};fs.forEach(f=>{(clients[f.client]=clients[f.client]||[]).push(f);});
    let h=`<div class="nkind">Tool / Tech</div><div class="ntitle">${esc(n.label)}</div>
      <div class="sub">appears in ${fs.length} files · ${Object.keys(clients).length} accounts</div>
      <div class="sec">Where it shows up</div>`;
    Object.keys(clients).sort((a,b)=>clients[b].length-clients[a].length).forEach(c=>{h+=`<div class="grp">${esc(c)}<span class="c">${clients[c].length}</span></div>`+clients[c].map(fileRow).join('');});
    panel.innerHTML=h;bindRows();
  } else if(n.type==='topic'){
    const ins=(instByTopic[n.label]||[]).slice().sort((a,b)=>a.label.localeCompare(b.label));
    const fs=filesByTopic[n.label]||[];
    let h=`<div class="nkind">Topic</div><div class="ntitle">${esc(n.label)}</div>
      <div class="sub">${ins.length} instructors · ${fs.length} files</div>`;
    if(ins.length)h+=`<div class="sec">Instructors — expert in this</div>`+ins.slice(0,120).map(instRow).join('');
    if(fs.length)h+=`<div class="sec">Files covering this topic</div>`+fs.slice(0,80).map(fileRow).join('');
    panel.innerHTML=h;bindInst();bindRows();
  } else if(n.type==='instructor'){
    const p=n;
    let h=`<div class="nkind">Instructor</div><div class="ntitle">${esc(p.label)}</div>`;
    if(p.role)h+=`<div class="sub" style="margin-top:4px">${esc(p.role)}</div>`;
    if(p.linkedin)h+=`<div><a class="linkedin" href="${esc(p.linkedin)}" target="_blank">in · LinkedIn ↗</a></div>`;
    if(p.topics&&p.topics.length)h+=`<div class="sec">Expert in (click to explore)</div><div class="chips">${(p.topics||[]).map(t=>`<span class="chip topic" data-tt="${esc(t)}">${esc(t)}</span>`).join('')}</div>`;
    if(p.expertise&&p.expertise.length)h+=`<div class="sec">Expertise</div><div class="chips">${chip(p.expertise,'inst')}</div>`;
    if(p.clients&&p.clients.length)h+=`<div class="sec">Proposed / appears for</div><div class="chips">${chip(p.clients,'')}</div>`;
    panel.innerHTML=h;bindTopicChips();
  } else if(n.type==='file'){
    const f=n;
    let h=`<div class="nkind">${esc(f.doctype||'File')} · ${esc(f.client)}</div><div class="ntitle">${esc(f.label)}</div>`;
    const meta=[f.program,f.version,f.duration,f.cohort?f.cohort+' participants':null].filter(Boolean);
    if(meta.length)h+=`<div class="chips" style="margin-top:8px">${meta.map(m=>`<span class="chip">${esc(m)}</span>`).join('')}</div>`;
    if(f.price_bands&&(f.price_bands.rates.length||f.price_bands.deals.length||f.price_bands.margin))h+=`<div class="sec">Pricing</div>${priceBands(f.price_bands)}`;
    if(f.topics&&f.topics.length)h+=`<div class="sec">Topics</div><div class="chips">${(f.topics||[]).map(t=>`<span class="chip topic" data-tt="${esc(t)}">${esc(t)}</span>`).join('')}</div>`;
    if(f.tools&&f.tools.length)h+=`<div class="sec">Tools / Tech</div><div class="chips">${chip(f.tools,'tool')}</div>`;
    h+=`<div class="sec">Location</div><div class="path">${esc(f.path)}</div>`;
    if(location.protocol==='file:')
      h+=`<div style="margin-top:10px"><a class="open" href="${encodeURI('./../../../'+f.path)}" target="_blank">↗ Open file</a></div>`;
    else
      h+=`<div style="margin-top:8px;font-size:11px;color:var(--mut)">Source file is on the local drive (not deployed).</div>`;
    if(f.client)h+=`<div style="margin-top:8px"><a class="open" href="#" id="back2c">← Back to ${esc(f.client)}</a></div>`;
    panel.innerHTML=h;bindTopicChips();
    const b=document.getElementById('back2c');if(b)b.onclick=ev=>{ev.preventDefault();nav(byId['C:'+f.client]);};
  }
}
function bindTopicChips(){panel.querySelectorAll('.chip[data-tt]').forEach(c=>c.onclick=()=>nav(byId['TP:'+c.dataset.tt]));}

// welcome state
panel.innerHTML=`<div class="empty"><h3>Click any node to drill in</h3>
  <div class="row"><span class="d" style="background:var(--client)"></span><div><b>Accounts</b> → programs run, pricing seen, tools, instructors proposed & every file.</div></div>
  <div class="row"><span class="d" style="background:var(--program)"></span><div><b>Programs</b> → which accounts run them, at what price, with which tools.</div></div>
  <div class="row"><span class="d" style="background:var(--topic)"></span><div><b>Topics</b> → instructors expert in it + files that cover it.</div></div>
  <div class="row"><span class="d" style="background:var(--instructor)"></span><div><b>Instructors</b> → bio, LinkedIn, expertise & accounts proposed for.</div></div>
  <div class="row"><span class="d" style="background:var(--tool)"></span><div><b>Tools</b> → every place a tech shows up across accounts.</div></div>
  <br>Use the filter pills to toggle layers, or the search box to jump straight to anything.</div>`;
</script></body></html>"""

html = HTML.replace("__DATA__", DATA).replace("__LOGO__", LOGO_B64)
with open(os.path.join(OUT, "graph.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("wrote graph.html", round(len(html)/1024), "KB  · logo embedded:", bool(LOGO_B64))
