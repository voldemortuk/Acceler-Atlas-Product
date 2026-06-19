#!/usr/bin/env python3
"""Delivered-Programs Curriculum Graph — same engine/format as the Pre-Sales KG
(_kg/build_html.py): self-contained canvas force-graph, dark Acceler theme,
top-bar stats, search, filter pills, drill-down side panel.
Node types: client · program · module · topic · tool. Built from the downloaded
'B2B AI Programs' folder. Keeps the pre-sales KG untouched."""
import os, re, json, base64

SRC  = "/Users/voldemort/Downloads/B2B AI Programs"
KG   = "/Users/voldemort/Downloads/1. PowerUp/APR - Pre-Sales Product/Knowledge Graph"
OUT  = os.path.join(KG, "curriculum-graph.html")
LOGO = os.path.join(KG, "deploy", "acceler_logo.png")

SKIP_TOP = {"Agentic AI & GenAI Resources ( B2C Programs )"}
IGNORE = {".ds_store","orientation","closing ceremony","closing ceremony ","archived",
          "uplevel shared","pre & post class assessments","virtual labs setup",
          "modules [old copy]","old copy"}
def ig(name): return name.lower().strip() in IGNORE or name.startswith(".") or "vm & ai tools setup" in name.lower()

TOOL_PAT = {
    "Claude Code": r"claude code", "Claude": r"claude", "ChatGPT/GPT": r"chatgpt|gpt|openai",
    "Copilot": r"copilot", "Gemini": r"gemini", "n8n": r"n8n", "LangGraph": r"langgraph",
    "LangChain": r"langchain", "CrewAI": r"crew", "Power Automate": r"power automate",
    "Make": r"\bmake\b|zapier", "Lovable": r"lovable", "Cursor": r"cursor",
    "Vector DB": r"vector|pinecone|chroma|faiss", "Azure": r"azure",
}
TOPIC_PAT = {
    "Prompting": r"prompt", "RAG": r"\brag\b|retrieval", "Agents": r"\bagent", "Multi-Agent": r"multi.?agent",
    "MCP / A2A": r"\bmcp\b|a2a", "Vector DB": r"vector|pinecone|chroma|faiss", "Fine-tuning": r"fine.?tun|lora|peft",
    "No-Code Agents": r"no.?code", "Low-Code": r"low.?code", "AI Coding": r"coding|vibe|bug.?fix",
    "Product / PRD": r"\bprd\b|product|roadmap", "Workflow Automation": r"workflow|automat",
    "Deployment": r"deploy|production|fastapi", "Responsible AI": r"responsible|ethic|governance",
    "Capstone": r"capstone|agentic fest|showcase|demo day", "LLM Foundations": r"\bllm\b|foundation|fundamental",
}
def client_of(p):
    n=p.lower()
    for k,v in {"e&":"e&","etisalat":"e&","ppf":"e&","cornerstone":"Cornerstone","bosch":"Bosch",
                "deloitte":"Deloitte","ets":"ETS","lowe":"Lowe's","nucleus":"Nucleus","yettel":"Yettel"}.items():
        if k in n: return v
    return p.split()[0]
def track_of(p):
    n=p.lower()
    for k,v in {"pro code":"Pro-Code","low code":"Low-Code","no code":"No-Code","leader":"Leaders",
                "sales":"Enablers","pms":"Navigators","enabler":"Enablers","builder":"Builders",
                "masterclass":"Masterclass","pilot":"Pilot"}.items():
        if k in n: return v
    return "Custom"
def clean(s):
    s=re.sub(r"\.(pptx|pdf|docx?|ipynb|key|mp4|png|jpg|jpeg|xlsx?|txt|csv)$","",s,flags=re.I)
    return re.sub(r"[_]+"," ",s).strip()

nodes={}; edges=[]; seen_edge=set()
def add(nid,**kw):
    if nid in nodes:
        nodes[nid]["count"]=nodes[nid].get("count",1)+kw.get("inc",0)
        return
    kw.pop("inc",None); nodes[nid]={"id":nid,**kw}
def E(a,b,rel="link"):
    k=(a,b)
    if k in seen_edge or a not in nodes or b not in nodes: return
    seen_edge.add(k); edges.append({"source":a,"target":b,"rel":rel})

programs=[d for d in sorted(os.listdir(SRC))
          if os.path.isdir(os.path.join(SRC,d)) and d not in SKIP_TOP and not d.startswith(".")]

for prog in programs:
    ppath=os.path.join(SRC,prog)
    pname=clean(prog).replace("B2B ","")
    cl=client_of(prog); tr=track_of(prog)
    pid="P:"+prog; cid="C:"+cl
    blob=(" ".join(n.lower() for _,_,fs in os.walk(ppath) for n in fs)+" "+prog.lower())
    mods=[m for m in sorted(os.listdir(ppath)) if os.path.isdir(os.path.join(ppath,m)) and not ig(m)]
    add(pid,type="program",label=pname,count=max(1,len(mods)),client=cl,track=tr,path=prog)
    add(cid,type="client",label=cl,count=0); nodes[cid]["count"]+=1; E(cid,pid,"runs")
    # modules (capture real files for open/download links)
    for m in mods:
        mid=pid+"|M:"+m
        mpath=os.path.join(ppath,m)
        files=[]
        for root,ds,fs in os.walk(mpath):
            ds[:]=[d for d in ds if not ig(d)]
            for f in sorted(fs):
                if f.startswith(".") or f.lower() in ("icon\r","icon"): continue
                rel=os.path.relpath(os.path.join(root,f),SRC)
                ext=os.path.splitext(f)[1].lstrip(".").lower()
                files.append({"name":clean(f),"ext":ext,"rel":rel})
            if len(files)>=30: break
        add(mid,type="module",label=clean(m),count=max(1,len(files)),program=pname,
            path=os.path.join(prog,m),files=files[:30])
        E(pid,mid,"has")
    # topics (concept-level, shared across programs)
    for t,pat in TOPIC_PAT.items():
        if re.search(pat,blob):
            tid="TP:"+t; add(tid,type="topic",label=t,count=0); nodes[tid]["count"]+=1; E(pid,tid,"covers")
    # tools
    for t,pat in TOOL_PAT.items():
        if re.search(pat,blob):
            xid="X:"+t; add(xid,type="tool",label=t,count=0); nodes[xid]["count"]+=1; E(pid,xid,"uses")

byid={n["id"]:n for n in nodes.values()}
def cnt(tp): return sum(1 for n in nodes.values() if n["type"]==tp)
meta={"programs":cnt("program"),"clients":cnt("client"),"modules":cnt("module"),
      "topics":cnt("topic"),"tools":cnt("tool")}
G={"nodes":list(nodes.values()),"edges":edges,"meta":meta}
DATA=json.dumps(G,ensure_ascii=False)
LOGO_B64=""
if os.path.exists(LOGO):
    LOGO_B64="data:image/png;base64,"+base64.b64encode(open(LOGO,"rb").read()).decode()

HTML=r"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Acceler · Delivered Programs · Curriculum Graph</title>
<style>
:root{--navy:#27B4E6;--navy2:#9FD9F2;--cyan:#27B4E6;--ink:#E8EDF9;--mut:#9AA6C8;
 --line:#243161;--line2:#1B2750;--bg:#0B1228;--panel:#121B3A;--soft:#1A2750;--cyansoft:#13343f;
 --client:#3FA9F5;--program:#F0A64E;--module:#9A8CFF;--topic:#43C8DE;--tool:#7FE0A4;
 --font:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;}
*{box-sizing:border-box}html,body{margin:0;height:100%;font-family:var(--font);background:var(--bg);color:var(--ink);overflow:hidden}
#app{display:flex;flex-direction:column;height:100vh}
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
#graphwrap{position:relative;flex:1;background:radial-gradient(circle at 32% 18%,#16204a 0%,var(--bg) 72%)}
canvas{display:block;cursor:grab}canvas:active{cursor:grabbing}
#tip{position:absolute;pointer-events:none;background:#020615;color:#fff;font-size:11.5px;padding:5px 9px;border-radius:7px;opacity:0;transition:opacity .1s;white-space:nowrap;z-index:30;box-shadow:0 6px 18px rgba(0,0,0,.45);border:1px solid var(--line)}
#ctrls{position:absolute;left:16px;bottom:14px;display:flex;gap:7px}
.cbtn{width:34px;height:34px;border-radius:9px;border:1px solid var(--line);background:var(--panel);color:var(--cyan);font-size:17px;font-weight:700;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.3)}
.cbtn:hover{border-color:var(--cyan);background:var(--soft)}
#hint{position:absolute;right:16px;bottom:14px;font-size:11px;color:var(--mut);background:rgba(10,16,40,.8);padding:6px 11px;border-radius:8px;border:1px solid var(--line)}
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
.flt{display:flex;align-items:center;gap:7px;font-size:11.5px;font-weight:600;color:var(--ink);cursor:pointer;user-select:none;background:var(--soft);border:1px solid var(--line);border-radius:20px;padding:5px 12px 5px 9px}
.flt:hover{border-color:var(--cyan)}.flt .dot{width:10px;height:10px;border-radius:50%;flex-shrink:0}
.flt.off{background:transparent;border-color:var(--line2);color:var(--mut)}.flt.off .dot{background:transparent!important;box-shadow:inset 0 0 0 2px var(--mut)}
.flt .dot.client{background:var(--client)}.flt .dot.program{background:var(--program)}.flt .dot.module{background:var(--module)}.flt .dot.topic{background:var(--topic)}.flt .dot.tool{background:var(--tool)}
#panel{flex:1;overflow:auto;padding:14px 18px 40px}
.empty{color:var(--mut);font-size:13px;line-height:1.7}.empty h3{color:var(--ink);font-size:14px;margin:0 0 8px}
.empty .row{display:flex;gap:8px;align-items:flex-start;margin:7px 0}.empty .row .d{width:9px;height:9px;border-radius:50%;margin-top:4px;flex-shrink:0}
.nkind{font-size:10.5px;text-transform:uppercase;letter-spacing:.1em;font-weight:800;color:var(--cyan)}
.ntitle{font-size:19px;font-weight:800;margin:4px 0 3px;line-height:1.25;color:var(--navy)}
.sub{font-size:12px;color:var(--mut);line-height:1.5}
.sec{font-size:10.5px;text-transform:uppercase;letter-spacing:.09em;color:var(--mut);font-weight:800;margin:18px 0 8px;padding-bottom:5px;border-bottom:1px solid var(--line)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{background:var(--soft);border:1px solid var(--line);border-radius:20px;padding:4px 10px;font-size:11.5px;color:var(--navy2);font-weight:600;cursor:pointer}
.chip.tool{background:#12321f;border-color:#225437;color:#7fe0a4}.chip.topic{background:#13343f;border-color:#1f5560;color:#9ee6f3}
.chip.track{background:#241f47;border-color:#3f377a;color:#bcb0f5}
.grp{font-size:12px;font-weight:800;color:var(--navy2);margin:14px 0 3px;display:flex;justify-content:space-between}
.grp .c{color:var(--mut);font-weight:600;font-size:11px}
.frow{display:flex;justify-content:space-between;gap:8px;padding:7px 0;border-bottom:1px solid var(--line2);cursor:pointer}
.frow:hover{background:var(--soft);margin:0 -8px;padding:7px 8px;border-radius:6px}
.fname{font-size:12.5px;color:var(--ink);line-height:1.35}.fmeta{font-size:11px;color:var(--mut);margin-top:3px}
.pill{display:inline-block;background:var(--bg);border:1px solid var(--line);border-radius:5px;padding:1px 6px;font-size:10px;color:var(--mut);margin-right:4px;margin-top:3px}
.backbar{display:flex;align-items:center;gap:6px;cursor:pointer;color:var(--navy2);font-size:12px;font-weight:700;padding:8px 11px;margin-bottom:12px;background:var(--soft);border:1px solid var(--line);border-radius:8px}
.backbar:hover{border-color:var(--cyan);color:var(--cyan)}
.open{color:var(--cyan);text-decoration:none;font-size:12px;font-weight:700}.open:hover{text-decoration:underline}
.dl{display:flex;gap:10px;flex-wrap:wrap;margin:10px 0 2px}
.frow a.open{flex-shrink:0;align-self:center}
.note{font-size:11px;color:var(--mut);margin-top:6px}
::-webkit-scrollbar{width:9px}::-webkit-scrollbar-thumb{background:#2A3866;border-radius:6px}::-webkit-scrollbar-track{background:transparent}
</style></head><body>
<div id="app">
 <div id="top">
   <img class="logo" src="__LOGO__" alt="Acceler"/>
   <div class="ttl"><b>Delivered Programs · Curriculum Graph</b><span>Clients · Programs · Modules · Topics · Tools</span></div>
   <div id="stats"></div>
 </div>
 <div id="main">
   <div id="graphwrap"><canvas id="cv"></canvas><div id="tip"></div>
     <div id="ctrls"><button class="cbtn" id="zin">+</button><button class="cbtn" id="zout">−</button><button class="cbtn" id="reset">⤾</button></div>
     <div id="hint">drag node · scroll = zoom · click = details · drag canvas = pan</div>
   </div>
   <div id="side">
     <div id="search"><span class="mag">⌕</span><input id="q" placeholder="Search a client, program, module, topic, tool…" autocomplete="off"/><div id="results"></div></div>
     <div class="filters" id="filters"></div>
     <div id="panel"></div>
   </div>
 </div>
</div>
<script>
const G=__DATA__;
const byId={};G.nodes.forEach(n=>byId[n.id]=n);
const ROOT='../../../B2B AI Programs/';
const DRIVE='https://drive.google.com/drive/u/1/folders/1tUMBGWfAKPzKA4hndaDjBe9hOHzMhza2';
const LOCAL=location.protocol==='file:';
function encRel(rel){return rel.split('/').map(encodeURIComponent).join('/');}
function localLink(rel,label){return LOCAL&&rel?`<a class="open" target="_blank" href="${ROOT+encRel(rel)}">↗ ${esc(label)}</a>`:'';}
function driveLink(label){return `<a class="open" target="_blank" href="${DRIVE}">↗ ${esc(label||'Open in Drive')}</a>`;}
function fileRow(f){const href=LOCAL?ROOT+encRel(f.rel):DRIVE;
  return `<div class="frow"><div><div class="fname">${esc(f.name)}</div><div class="fmeta"><span class="pill">${esc(f.ext||'file')}</span></div></div><a class="open" target="_blank" href="${esc(href)}">↗ Open</a></div>`;}
const edgesByType=(id,t,dir)=>G.edges.filter(e=>(dir==='out'?e.source===id:e.target===id)).map(e=>byId[dir==='out'?e.target:e.source]).filter(n=>n&&n.type===t);
const M=G.meta;
document.getElementById('stats').innerHTML=[['clients',M.clients],['programs',M.programs],['modules',M.modules],['topics',M.topics],['tools',M.tools]]
  .map(([l,v])=>`<div class="stat"><b>${v}</b><span>${l}</span></div>`).join('');
const COL={client:'#3FA9F5',program:'#F0A64E',module:'#9A8CFF',topic:'#43C8DE',tool:'#7FE0A4'};
const show={client:true,program:true,module:true,topic:true,tool:false};
const filters=document.getElementById('filters');
[['client','Clients'],['program','Programs'],['module','Modules'],['topic','Topics'],['tool','Tools']].forEach(([k,lab])=>{
  const el=document.createElement('div');el.className='flt'+(show[k]?'':' off');
  el.innerHTML=`<span class="dot ${k}"></span>${lab}`;
  el.onclick=()=>{show[k]=!show[k];el.classList.toggle('off');layoutInit();};filters.appendChild(el);});
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');let W,H,DPR=window.devicePixelRatio||1;
function resize(){const r=cv.parentElement.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*DPR;cv.height=H*DPR;cv.style.width=W+'px';cv.style.height=H+'px';ctx.setTransform(DPR,0,0,DPR,0,0);}
window.addEventListener('resize',resize);resize();
let view={x:W/2,y:H/2,k:0.8};let N=[],Edr=[],sel=null,hover=null,drag=null,panning=false,last=null,alpha=1;
function layoutInit(){N=G.nodes.filter(n=>show[n.type]);const ids=new Set(N.map(n=>n.id));
  Edr=G.edges.filter(e=>ids.has(e.source)&&ids.has(e.target));
  N.forEach((n,i)=>{if(n.x===undefined){const a=i*2.399,r=40+Math.sqrt(i)*46;n.x=Math.cos(a)*r;n.y=Math.sin(a)*r;n.vx=0;n.vy=0;}});alpha=1;}
function rad(n){const c=Math.sqrt(n.count||1);if(n.type==='client')return 8+Math.min(16,c*2);if(n.type==='program')return 8+Math.min(15,c*2);if(n.type==='topic'||n.type==='tool')return 6+Math.min(13,c);return 5+Math.min(9,c);}
layoutInit();
function tick(){for(let i=0;i<N.length;i++){const a=N[i];for(let j=i+1;j<N.length;j++){const b=N[j];let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+0.01;if(d2<90000){let f=460/d2;a.vx+=dx*f;a.vy+=dy*f;b.vx-=dx*f;b.vy-=dy*f;}}a.vx-=a.x*0.0016;a.vy-=a.y*0.0016;}
  Edr.forEach(e=>{const a=byId[e.source],b=byId[e.target];if(a.x===undefined||b.x===undefined)return;let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)||1;let f=(d-78)*0.02;let fx=dx/d*f,fy=dy/d*f;a.vx+=fx;a.vy+=fy;b.vx-=fx;b.vy-=fy;});
  N.forEach(n=>{if(n===drag)return;n.x+=n.vx*alpha;n.y+=n.vy*alpha;n.vx*=0.86;n.vy*=0.86;});if(alpha>0.02)alpha*=0.994;}
function toScreen(n){return{x:view.x+n.x*view.k,y:view.y+n.y*view.k};}
function neighbor(n){return sel&&(n===sel||Edr.some(e=>(e.source===sel.id&&e.target===n.id)||(e.target===sel.id&&e.source===n.id)));}
function draw(){ctx.clearRect(0,0,W,H);
  Edr.forEach(e=>{const a=byId[e.source],b=byId[e.target],pa=toScreen(a),pb=toScreen(b);const hot=sel&&(e.source===sel.id||e.target===sel.id);
    ctx.strokeStyle=hot?'rgba(39,180,230,.5)':'rgba(120,135,180,.12)';ctx.lineWidth=hot?1.7:1;ctx.beginPath();ctx.moveTo(pa.x,pa.y);ctx.lineTo(pb.x,pb.y);ctx.stroke();});
  N.forEach(n=>{const p=toScreen(n),r=rad(n)*Math.max(.6,Math.min(1.4,view.k)),dim=sel&&!neighbor(n);
    ctx.globalAlpha=dim?0.22:1;ctx.beginPath();ctx.arc(p.x,p.y,r,0,7);ctx.fillStyle=COL[n.type];ctx.fill();
    if(n===sel){ctx.lineWidth=3;ctx.strokeStyle='#fff';ctx.stroke();}else if(n===hover){ctx.lineWidth=2;ctx.strokeStyle='#fff';ctx.stroke();}
    if(view.k>0.7||n.type==='client'||n.type==='program'||n===hover||n===sel){ctx.globalAlpha=dim?0.3:1;ctx.fillStyle=n.type==='client'?'#eaf3ff':'#b9c4e6';
      ctx.font=(n.type==='client'||n.type==='program'?'700 ':'600 ')+Math.round(11.5*Math.min(1.2,Math.max(.85,view.k)))+'px '+getComputedStyle(document.body).fontFamily;
      let lab=n.label.length>30?n.label.slice(0,29)+'…':n.label;ctx.fillText(lab,p.x+r+4,p.y+4);}ctx.globalAlpha=1;});}
function loop(){tick();draw();requestAnimationFrame(loop);}loop();
function pick(mx,my){let best=null,bd=18;for(const n of N){const p=toScreen(n),d=Math.hypot(p.x-mx,p.y-my);if(d<bd+rad(n)&&d<bd){bd=d;best=n;}}return best;}
const tip=document.getElementById('tip');
cv.addEventListener('mousedown',e=>{const m=rel(e),n=pick(m.x,m.y);if(n){drag=n;nav(n);}else panning=true;last=m;});
window.addEventListener('mousemove',e=>{const m=rel(e);if(drag){drag.x=(m.x-view.x)/view.k;drag.y=(m.y-view.y)/view.k;alpha=Math.max(alpha,.4);tip.style.opacity=0;}
  else if(panning){view.x+=m.x-last.x;view.y+=m.y-last.y;}else{hover=pick(m.x,m.y);cv.style.cursor=hover?'pointer':'grab';
    if(hover){tip.textContent=hover.label;tip.style.left=(m.x+14)+'px';tip.style.top=(m.y+12)+'px';tip.style.opacity=1;}else tip.style.opacity=0;}last=m;});
window.addEventListener('mouseup',()=>{drag=null;panning=false;});
cv.addEventListener('wheel',e=>{e.preventDefault();const m=rel(e),f=Math.exp(-e.deltaY*0.0012);view.x=m.x-(m.x-view.x)*f;view.y=m.y-(m.y-view.y)*f;view.k*=f;view.k=Math.max(.15,Math.min(4,view.k));},{passive:false});
function rel(e){const r=cv.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top};}
function zoomBy(f){view.x=W/2-(W/2-view.x)*f;view.y=H/2-(H/2-view.y)*f;view.k=Math.max(.15,Math.min(4,view.k*f));}
document.getElementById('zin').onclick=()=>zoomBy(1.25);document.getElementById('zout').onclick=()=>zoomBy(.8);
document.getElementById('reset').onclick=()=>{view={x:W/2,y:H/2,k:0.8};};
const qbox=document.getElementById('q'),results=document.getElementById('results');
qbox.addEventListener('input',e=>{const q=e.target.value.toLowerCase().trim();if(!q){results.style.display='none';return;}
  const hits=G.nodes.filter(n=>n.label.toLowerCase().includes(q)).slice(0,40);if(!hits.length){results.style.display='none';return;}
  results.innerHTML=hits.map(n=>`<div class="r" data-id="${esc(n.id)}"><span class="k" style="background:${COL[n.type]}">${n.type.slice(0,4)}</span>${esc(n.label)}</div>`).join('');
  results.style.display='block';results.querySelectorAll('.r').forEach(r=>r.onclick=()=>{results.style.display='none';qbox.value='';nav(byId[r.dataset.id]);});});
document.addEventListener('click',e=>{if(!document.getElementById('search').contains(e.target))results.style.display='none';});
const panel=document.getElementById('panel');
function esc(s){return(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));}
function row(n,meta){return `<div class="frow" data-id="${esc(n.id)}"><div><div class="fname">${esc(n.label)}</div>${meta?`<div class="fmeta">${esc(meta)}</div>`:''}</div></div>`;}
function chips(arr,cls){return `<div class="chips">${arr.map(n=>`<span class="chip ${cls}" data-id="${esc(n.id)}">${esc(n.label)}</span>`).join('')}</div>`;}
function bind(){panel.querySelectorAll('[data-id]').forEach(r=>r.onclick=()=>nav(byId[r.dataset.id]));}
let navHist=[],cur=null;
function nav(n){if(!n)return;if(cur&&cur.id!==n.id)navHist.push(cur);cur=n;sel=n;render(n);back();panel.scrollTop=0;}
function back(){if(!navHist.length)return;const p=navHist[navHist.length-1],lab=p.label.length>34?p.label.slice(0,33)+'…':p.label;
  const b=document.createElement('div');b.className='backbar';b.textContent='← Back to '+lab;b.onclick=()=>{cur=navHist.pop();sel=cur;render(cur);back();panel.scrollTop=0;};panel.insertBefore(b,panel.firstChild);}
function render(n){
  if(n.type==='client'){const progs=edgesByType(n.id,'program','out');
    const tools=[...new Set(progs.flatMap(p=>edgesByType(p.id,'tool','out').map(t=>t.id)))].map(id=>byId[id]);
    const tops=[...new Set(progs.flatMap(p=>edgesByType(p.id,'topic','out').map(t=>t.id)))].map(id=>byId[id]);
    let h=`<div class="nkind">Client</div><div class="ntitle">${esc(n.label)}</div><div class="sub">${progs.length} delivered programs</div>`;
    if(tops.length)h+=`<div class="sec">Topics covered</div>${chips(tops,'topic')}`;
    if(tools.length)h+=`<div class="sec">Tools used</div>${chips(tools,'tool')}`;
    h+=`<div class="sec">Programs delivered</div>`+progs.map(p=>row(p,p.track+' · '+(p.count)+' modules')).join('');panel.innerHTML=h;bind();}
  else if(n.type==='program'){const mods=edgesByType(n.id,'module','out'),tools=edgesByType(n.id,'tool','out'),tops=edgesByType(n.id,'topic','out'),cl=edgesByType(n.id,'client','in')[0];
    let h=`<div class="nkind">Program · ${esc(n.track||'')}</div><div class="ntitle">${esc(n.label)}</div><div class="sub">${cl?esc(cl.label)+' · ':''}${mods.length} modules</div>`;
    h+=`<div class="dl">${localLink(n.path,'Open program folder')}${driveLink('B2B AI Programs (Drive)')}</div>`;
    if(!LOCAL)h+=`<div class="note">Local files open when this graph is run from the drive; deployed, links go to the Drive folder.</div>`;
    if(tops.length)h+=`<div class="sec">Topics</div>${chips(tops,'topic')}`;
    if(tools.length)h+=`<div class="sec">Tools / Tech</div>${chips(tools,'tool')}`;
    if(mods.length)h+=`<div class="sec">Modules</div>`+mods.map(m=>row(m,m.count+' items')).join('');panel.innerHTML=h;bind();}
  else if(n.type==='module'){const prog=edgesByType(n.id,'program','in')[0];
    let h=`<div class="nkind">Module</div><div class="ntitle">${esc(n.label)}</div><div class="sub">${prog?esc(prog.label):''} · ${(n.files||[]).length} files</div>`;
    h+=`<div class="dl">${localLink(n.path,'Open module folder')}${driveLink('Drive')}</div>`;
    if(prog)h+=`<div class="sec">Part of</div>${chips([prog],'track')}`;
    if(n.files&&n.files.length)h+=`<div class="sec">Files · open / download</div>`+n.files.map(fileRow).join('');
    panel.innerHTML=h;bind();}
  else if(n.type==='topic'){const progs=edgesByType(n.id,'program','in');
    let h=`<div class="nkind">Topic</div><div class="ntitle">${esc(n.label)}</div><div class="sub">covered in ${progs.length} programs</div><div class="sec">Programs covering this</div>`+progs.map(p=>row(p,p.track)).join('');panel.innerHTML=h;bind();}
  else if(n.type==='tool'){const progs=edgesByType(n.id,'program','in');
    let h=`<div class="nkind">Tool / Tech</div><div class="ntitle">${esc(n.label)}</div><div class="sub">used in ${progs.length} programs</div><div class="sec">Programs using it</div>`+progs.map(p=>row(p,p.track)).join('');panel.innerHTML=h;bind();}
}
panel.innerHTML=`<div class="empty"><h3>Click any node to drill in</h3>
  <div class="row"><span class="d" style="background:var(--client)"></span><div><b>Clients</b> → every program delivered, topics & tools.</div></div>
  <div class="row"><span class="d" style="background:var(--program)"></span><div><b>Programs</b> → modules, topics, tools, track.</div></div>
  <div class="row"><span class="d" style="background:var(--module)"></span><div><b>Modules</b> → the day/module breakdown.</div></div>
  <div class="row"><span class="d" style="background:var(--topic)"></span><div><b>Topics</b> → which programs cover them.</div></div>
  <div class="row"><span class="d" style="background:var(--tool)"></span><div><b>Tools</b> → where each tech shows up.</div></div>
  <br>Toggle layers with the pills, or search to jump anywhere.</div>`;
</script></body></html>"""
html=HTML.replace("__DATA__",DATA).replace("__LOGO__",LOGO_B64)
open(OUT,"w",encoding="utf-8").write(html)
print("nodes:",len(nodes),"edges:",len(edges),"| meta:",meta,"| logo:",bool(LOGO_B64))
print("wrote",OUT,round(len(html)/1024),"KB")
