#!/usr/bin/env python3
"""Threat Actors Generator v5. Pure template engine. All data from JSON. Images from folder with SVG fallback."""
import json,os,glob,hashlib,shutil
from html import escape
BASE=os.path.dirname(os.path.abspath(__file__))
DATA=os.path.join(BASE,'data','actors');IMG_IN=os.path.join(DATA,'images')
CONTRIB_FILE=os.path.join(BASE,'data','contributors.json')
CONTRIB_IMG=os.path.join(BASE,'data','contributors','images')
SPONSORS_FILE=os.path.join(BASE,'data','sponsors.json')
SPONSORS_IMG=os.path.join(BASE,'data','sponsors','images')
OUT=BASE;IMG_OUT=os.path.join(BASE,'images','actors')
CONTRIB_IMG_OUT=os.path.join(BASE,'images','contributors')
SPONSORS_IMG_OUT=os.path.join(BASE,'images','sponsors')
def fmt_html(html):
    """Format HTML with proper line breaks and indentation."""
    import re
    tags_newline = ['<!DOCTYPE','<html','</html>','<head','</head>','<body','</body>',
        '<nav','</nav>','<section','</section>','<footer','</footer>',
        '<div class="content-section','<div class="actor-hero','<div class="actor-below',
        '<div class="breadcrumb','<div class="filter-bar','<div class="cards-section',
        '<div class="cards-grid','<div class="hero','<div class="info-card',
        '<div class="detail-grid','<div class="campaign-timeline',
        '<table','</table>','<thead','</thead>','<tbody','</tbody>',
        '<ul class="ref-list','</ul>','<h1','<h2','<iframe','<script','</script>',
        '<svg','</svg>','<div id="page-search']
    for tag in tags_newline:
        html = html.replace(tag, '\n' + tag)
    html = html.replace('</div></div></div></div>', '</div>\n</div>\n</div>\n</div>')
    lines = [l for l in html.split('\n') if l.strip()]
    return '\n'.join(lines) + '\n'

SITE="Threat Actor Profiles";EXTS=('.png','.jpg','.jpeg','.svg','.webp')

def load():
    a=[]
    for fp in sorted(glob.glob(os.path.join(DATA,'*.json'))):
        with open(fp,'r') as f: a.append(json.load(f))
    return a

def load_json(fp):
    if os.path.isfile(fp):
        with open(fp,'r') as f: return json.load(f)
    return []

def copy_dir_images(src,dst):
    os.makedirs(dst,exist_ok=True)
    if os.path.isdir(src):
        for f in os.listdir(src):
            s=os.path.join(src,f)
            if os.path.isfile(s): shutil.copy2(s,os.path.join(dst,f))

def bc(t):
    t=t.lower()
    if 'criminal' in t and ('state' in t or 'hybrid' in t): return 'badge-hybrid'
    if 'criminal' in t: return 'badge-criminal'
    return 'badge-nation'

def fimg(aid):
    for e in EXTS:
        if os.path.isfile(os.path.join(IMG_IN,f"{aid}{e}")): return f"{aid}{e}"
    return None

def cpimg():
    os.makedirs(IMG_OUT,exist_ok=True)
    if os.path.isdir(IMG_IN):
        for f in os.listdir(IMG_IN):
            s=os.path.join(IMG_IN,f)
            if os.path.isfile(s): shutil.copy2(s,os.path.join(IMG_OUT,f))

def fsvg(aid,name,w=400,h=300):
    hsh=int(hashlib.md5(aid.encode()).hexdigest()[:8],16);ac='#604ca9'
    figs=[f'<path d="M{w//2-45} {h-60} Q{w//2-45} {h//2+20} {w//2} {h//2-20} Q{w//2+45} {h//2+20} {w//2+45} {h-60}" fill="{ac}" opacity="0.15"/><path d="M{w//2-35} {h-55} Q{w//2-35} {h//2+30} {w//2} {h//2-10} Q{w//2+35} {h//2+30} {w//2+35} {h-55}" fill="none" stroke="{ac}" stroke-width="1.5" opacity="0.6"/><circle cx="{w//2-12}" cy="{h//2+15}" r="3" fill="{ac}" opacity="0.8"/><circle cx="{w//2+12}" cy="{h//2+15}" r="3" fill="{ac}" opacity="0.8"/>',f'<path d="M{w//2-30} {h-50} Q{w//2-50} {h//2} {w//2-20} {h//2-30} Q{w//2+10} {h//2-45} {w//2+40} {h//2-20} Q{w//2+50} {h//2+10} {w//2+30} {h-50}" fill="{ac}" opacity="0.12"/><path d="M{w//2-25} {h-45} Q{w//2-40} {h//2+5} {w//2-15} {h//2-25} Q{w//2+10} {h//2-38} {w//2+35} {h//2-15} Q{w//2+42} {h//2+10} {w//2+25} {h-45}" fill="none" stroke="{ac}" stroke-width="1.5" opacity="0.5"/><circle cx="{w//2+5}" cy="{h//2+5}" r="4" fill="{ac}" opacity="0.7"/>',f'<rect x="{w//2-40}" y="{h//2-25}" width="80" height="50" rx="8" fill="{ac}" opacity="0.1"/><rect x="{w//2-35}" y="{h//2-20}" width="70" height="40" rx="6" fill="none" stroke="{ac}" stroke-width="1.2" opacity="0.5"/><line x1="{w//2-20}" y1="{h//2}" x2="{w//2-8}" y2="{h//2}" stroke="{ac}" stroke-width="2" opacity="0.8" stroke-linecap="round"/><line x1="{w//2+8}" y1="{h//2}" x2="{w//2+20}" y2="{h//2}" stroke="{ac}" stroke-width="2" opacity="0.8" stroke-linecap="round"/>']
    fig=figs[hsh%len(figs)]
    ls=''.join(f'<line x1="{((hsh+i*73)%(w-40))+20}" y1="{((hsh+i*41)%(h-40))+20}" x2="{((hsh+i*97)%(w-40))+20}" y2="{((hsh+i*53)%(h-40))+20}" stroke="{ac}" stroke-width="0.5" opacity="0.08"/>' for i in range(8))
    ns=''.join(f'<circle cx="{((hsh+i*67)%(w-30))+15}" cy="{((hsh+i*89)%(h-30))+15}" r="{((hsh+i*11)%3)+1}" fill="{ac}" opacity="{0.1+((hsh+i*31)%15)/100:.2f}"/>' for i in range(12))
    nm=name[:6].upper()
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" preserveAspectRatio="xMidYMid slice"><rect width="{w}" height="{h}" fill="#0a0f1e"/><defs><radialGradient id="g-{aid}" cx="50%" cy="40%"><stop offset="0%" stop-color="{ac}" stop-opacity="0.15"/><stop offset="100%" stop-color="#0a0f1e" stop-opacity="0"/></radialGradient></defs><rect width="{w}" height="{h}" fill="url(#g-{aid})" opacity="0.4"/>{ls}{ns}<text x="{w//2}" y="{h-15}" font-family="Chivo,sans-serif" font-size="48" font-weight="900" fill="{ac}" opacity="0.04" text-anchor="middle" letter-spacing="8">{nm}</text>{fig}</svg>'

def cimg_html(a,w=400,h=300,d=0):
    im=fimg(a['id'])
    if im:
        p="../"*d
        return f'<img src="{p}images/actors/{im}" alt="{escape(a["name"])}" style="width:100%;height:100%;object-fit:cover;display:block">'
    # No image found - show empty placeholder with actor initials
    name=a.get('name','?')
    initials=''.join(w[0] for w in name.split()[:2]).upper()
    return f'<div style="width:100%;height:100%;background:#0a0f1e;display:flex;align-items:center;justify-content:center"><div style="font:900 6rem Chivo;color:rgba(96,76,169,0.15);letter-spacing:8px">{initials}</div></div>'

def afsvg(steps,camp):
    if not steps: return '<p style="color:var(--tm);font-size:1.5rem">No attack flow data.</p>'
    import json as _j
    uid="af"+str(abs(hash(camp)))[:6]
    tc_map={"initial access":"#4ecca3","execution":"#604ca9","persistence":"#7b68c4","privilege escalation":"#9b5de5","defense evasion":"#f4845f","credential access":"#ffd166","discovery":"#00d4ff","lateral movement":"#00d4ff","collection":"#a8b2c1","command & control":"#604ca9","command and control":"#604ca9","exfiltration":"#f4845f","impact":"#E91E63","resource development":"#E91E63"}
    cols=4;nw=280;nh=100;gx=40;gy=36;pad=24
    rows=(len(steps)+cols-1)//cols
    cw=pad*2+cols*nw+(cols-1)*gx
    ch=pad+52+rows*(nh+gy)+60
    nodes_json=[]
    for i,s in enumerate(steps):
        col,row=i%cols,i//cols
        x=pad+col*(nw+gx);y=pad+38+row*(nh+gy)
        tc=tc_map.get(s.get("tactic","").lower(),"#604ca9")
        nodes_json.append({"i":i,"x":x,"y":y,"tc":tc,"tactic":s.get("tactic",""),"step":s.get("step",""),"tid":s.get("tid",""),"desc":s.get("desc","")})
    nj=_j.dumps(nodes_json).replace("</","<\\/")
    JS="""(function(){var D=##NJ##;var W=##NW##,H=##NH##,ct=document.getElementById("##UID##nodes"),sv=document.getElementById("##UID##svg");function mkN(){ct.innerHTML="";D.forEach(function(n){var d=document.createElement("div");d.className="afn";d.dataset.idx=n.i;d.style.cssText="position:absolute;left:"+n.x+"px;top:"+n.y+"px;width:"+W+"px;height:"+H+"px;background:#1a1e23;border:1.5px solid "+n.tc+";border-radius:6px;cursor:grab;user-select:none;overflow:hidden;transition:box-shadow 0.2s";d.innerHTML='<div style="height:22px;background:'+n.tc+'15;display:flex;align-items:center;padding:0 8px"><span style="background:'+n.tc+';color:#fff;font:700 10px Chivo;padding:2px 7px;border-radius:3px;margin-right:6px">'+(n.i+1)+'</span><span style="font:700 10px Nunito Sans;color:'+n.tc+';letter-spacing:0.3px">'+n.tactic.toUpperCase().slice(0,24)+'</span></div><div style="padding:6px 10px"><div style="font:600 13px Chivo;color:#eee;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+n.step+'</div><div style="font:600 11px Nunito Sans;color:'+n.tc+';opacity:0.8;margin-top:2px">'+n.tid+'</div><div style="font:400 10px Nunito Sans;color:rgba(255,255,255,0.3);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+n.desc+'</div></div>';d.title=n.step+"\\n"+n.tactic+"\\n"+n.tid+"\\n"+n.desc;ct.appendChild(d)})}function mkE(){var s="";for(var i=1;i<D.length;i++){var a=D[i-1],b=D[i];var x1=a.x+W,y1=a.y+H/2,x2=b.x,y2=b.y+H/2;if(b.x<=a.x){x1=a.x+W/2;y1=a.y+H;x2=b.x+W/2;y2=b.y}var mx=(x1+x2)/2;var cyo=y1===y2?-45:0;s+='<path d="M'+x1+' '+y1+' C'+mx+' '+(y1+cyo)+' '+mx+' '+(y2+cyo)+' '+x2+' '+y2+'" fill="none" stroke="rgba(96,76,169,0.35)" stroke-width="1.5" stroke-dasharray="6 4"/>';s+='<polygon points="'+(x2-6)+','+(y2-4)+' '+x2+','+y2+' '+(x2-6)+','+(y2+4)+'" fill="rgba(96,76,169,0.5)"/>'}sv.innerHTML=s}mkN();mkE();var drag=null,ox=0,oy=0;ct.addEventListener("mousedown",function(e){var t=e.target.closest(".afn");if(!t)return;drag=t;var r=t.getBoundingClientRect();ox=e.clientX-r.left;oy=e.clientY-r.top;t.style.cursor="grabbing";t.style.zIndex=10;t.style.boxShadow="0 8px 32px rgba(96,76,169,0.3)";e.preventDefault()});document.addEventListener("mousemove",function(e){if(!drag)return;var p=ct.getBoundingClientRect();var nx=e.clientX-p.left-ox,ny=e.clientY-p.top-oy;drag.style.left=nx+"px";drag.style.top=ny+"px";var idx=+drag.dataset.idx;D[idx].x=nx;D[idx].y=ny;mkE()});document.addEventListener("mouseup",function(){if(drag){drag.style.cursor="grab";drag.style.zIndex=1;drag.style.boxShadow="none";drag=null}});ct.addEventListener("touchstart",function(e){var t=e.target.closest(".afn");if(!t)return;drag=t;var r=t.getBoundingClientRect();ox=e.touches[0].clientX-r.left;oy=e.touches[0].clientY-r.top;t.style.zIndex=10;e.preventDefault()},{passive:false});document.addEventListener("touchmove",function(e){if(!drag)return;var p=ct.getBoundingClientRect();var nx=e.touches[0].clientX-p.left-ox,ny=e.touches[0].clientY-p.top-oy;drag.style.left=nx+"px";drag.style.top=ny+"px";D[+drag.dataset.idx].x=nx;D[+drag.dataset.idx].y=ny;mkE()},{passive:false});document.addEventListener("touchend",function(){if(drag){drag.style.zIndex=1;drag=null}})})();"""
    JS=JS.replace("##NJ##",nj).replace("##NW##",str(nw)).replace("##NH##",str(nh)).replace("##UID##",uid)
    h='<div id="'+uid+'" style="position:relative;width:100%;overflow-x:auto;background:#121619;border-radius:6px;border:1px solid rgba(255,255,255,0.05)">'
    h+='<div id="'+uid+'w" style="position:relative;width:'+str(cw)+'px;height:'+str(ch)+'px;min-height:300px">'
    h+='<div style="position:absolute;left:'+str(pad)+'px;top:'+str(pad)+'px;right:'+str(pad)+'px;height:28px;background:rgba(96,76,169,0.06);border:1px solid rgba(96,76,169,0.15);border-radius:4px;display:flex;align-items:center;padding:0 14px">'
    h+='<span style="font-family:Chivo,sans-serif;font-size:13px;font-weight:700;color:#604ca9;letter-spacing:0.5px">ATTACK FLOW</span>'
    h+='<span style="font-family:Nunito Sans,sans-serif;font-size:12px;color:rgba(255,255,255,0.4);margin-left:16px">'+escape(camp)+'</span>'
    h+='<span style="font-family:Nunito Sans,sans-serif;font-size:11px;color:rgba(255,255,255,0.2);margin-left:auto">'+str(len(steps))+' steps | Drag nodes to rearrange</span></div>'
    h+='<svg id="'+uid+'svg" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none"></svg>'
    h+='<div id="'+uid+'nodes"></div></div></div>'
    h+='<script>'+JS+'</'+'script>'
    return h


def diamond_svg(dm):
    if not dm or not any(dm.values()): return ''
    adv=escape(dm.get('adversary','-'));inf=escape(dm.get('infrastructure','-'))
    cap=escape(dm.get('capability','-'));vic=escape(dm.get('victim','-'))
    uid="dm"+str(abs(hash(str(dm))))[:6]
    JS="""(function(){var ct=document.getElementById("##UID##n"),sv=document.getElementById("##UID##svg");var ns=[{id:0,x:170,y:30,w:80,h:36,label:"ADV",sub:"Adversary",c:"#604ca9",bg:"rgba(96,76,169,0.1)"},{id:1,x:170,y:354,w:80,h:36,label:"VIC",sub:"Victim",c:"#E91E63",bg:"rgba(233,30,99,0.08)"},{id:2,x:10,y:192,w:80,h:36,label:"CAP",sub:"Capability",c:"#4ecca3",bg:"rgba(78,204,163,0.08)"},{id:3,x:330,y:192,w:80,h:36,label:"INF",sub:"Infra",c:"#ffd166",bg:"rgba(255,209,102,0.08)"},{id:4,x:193,y:193,w:34,h:34,label:"E",sub:"Event",c:"#604ca9",bg:"rgba(96,76,169,0.15)"}];var edges=[[0,3],[3,1],[1,2],[2,0],[0,1],[2,3]];function mk(){ct.innerHTML="";ns.forEach(function(n){var d=document.createElement("div");d.dataset.idx=n.id;d.style.cssText="position:absolute;left:"+n.x+"px;top:"+n.y+"px;width:"+n.w+"px;height:"+n.h+"px;background:"+n.bg+";border:2px solid "+n.c+";border-radius:"+(n.id===4?"50%":"6px")+";cursor:grab;display:flex;flex-direction:column;align-items:center;justify-content:center;user-select:none;z-index:2;transition:box-shadow 0.2s";d.innerHTML='<span style="font:700 '+(n.id===4?'9':'11')+'px Chivo;color:'+n.c+'">'+n.label+'</span>'+(n.id!==4?'<span style="font:400 8px Nunito Sans;color:rgba(255,255,255,0.4)">'+n.sub+'</span>':'');d.title=n.sub;ct.appendChild(d)})}function mkE(){var s='<text x="210" y="18" font-family="Chivo" font-size="12" font-weight="700" fill="#604ca9" text-anchor="middle" letter-spacing="1">DIAMOND MODEL</text>';s+='<line x1="195" y1="100" x2="195" y2="320" stroke="#604ca9" stroke-width="0.5" opacity="0.08" stroke-dasharray="3 4"/>';s+='<line x1="60" y1="210" x2="370" y2="210" stroke="#604ca9" stroke-width="0.5" opacity="0.08" stroke-dasharray="3 4"/>';s+='<text x="207" y="150" font-family="Nunito Sans" font-size="7" fill="rgba(255,255,255,0.12)" letter-spacing="1" transform="rotate(-90,207,150)">SOCIAL-POLITICAL</text>';s+='<text x="270" y="222" font-family="Nunito Sans" font-size="7" fill="rgba(255,255,255,0.12)" letter-spacing="1">TECHNOLOGY</text>';edges.forEach(function(e,i){var a=ns[e[0]],b=ns[e[1]];var x1=a.x+a.w/2,y1=a.y+a.h/2,x2=b.x+b.w/2,y2=b.y+b.h/2;var dash=i>=4?"2 5":"5 4",op=i>=4?"0.08":"0.2";s+='<line x1="'+x1+'" y1="'+y1+'" x2="'+x2+'" y2="'+y2+'" stroke="#604ca9" stroke-width="1" opacity="'+op+'" stroke-dasharray="'+dash+'"/>'});sv.innerHTML=s}mk();mkE();var drag=null,ox=0,oy=0;ct.addEventListener("mousedown",function(e){var t=e.target.closest("[data-idx]");if(!t)return;drag=t;var r=t.getBoundingClientRect();ox=e.clientX-r.left;oy=e.clientY-r.top;t.style.cursor="grabbing";t.style.zIndex=10;t.style.boxShadow="0 4px 20px rgba(96,76,169,0.3)";e.preventDefault()});document.addEventListener("mousemove",function(e){if(!drag)return;var p=document.getElementById("##UID##").getBoundingClientRect();var nx=e.clientX-p.left-ox,ny=e.clientY-p.top-oy;drag.style.left=nx+"px";drag.style.top=ny+"px";var idx=+drag.dataset.idx;ns[idx].x=nx;ns[idx].y=ny;mkE()});document.addEventListener("mouseup",function(){if(drag){drag.style.cursor="grab";drag.style.zIndex=2;drag.style.boxShadow="none";drag=null}})})();"""
    JS=JS.replace("##UID##",uid)
    h='<div class="grid-2col-wide">'
    h+='<div id="'+uid+'" style="position:relative;width:420px;height:420px;background:#121619;border-radius:6px;border:1px solid rgba(255,255,255,0.05)">'
    h+='<svg id="'+uid+'svg" style="position:absolute;inset:0;width:100%;height:100%;pointer-events:none"></svg>'
    h+='<div id="'+uid+'n"></div>'
    h+='<div style="position:absolute;bottom:8px;left:0;right:0;text-align:center;font:8px Nunito Sans;color:rgba(255,255,255,0.15)">Caltagirone, Pendergast &amp; Betz (2013) | Drag to rearrange</div>'
    h+='</div>'
    h+='<div style="display:flex;flex-direction:column;gap:1.2rem">'
    h+='<div class="panel-purple"><div class="panel-label" style="color:#604ca9">ADVERSARY</div><div class="panel-body">'+adv+'</div></div>'
    h+='<div class="panel-green"><div class="panel-label" style="color:#4ecca3">CAPABILITY</div><div class="panel-body">'+cap+'</div></div>'
    h+='<div class="panel-yellow"><div class="panel-label" style="color:#ffd166">INFRASTRUCTURE</div><div class="panel-body">'+inf+'</div></div>'
    h+='<div class="panel-pink"><div class="panel-label" style="color:#E91E63">VICTIM</div><div class="panel-body">'+vic+'</div></div>'
    h+='</div></div>'
    h+='<script>'+JS+'</'+'script>'
    return h



def hd(t,d=0):
    p="../"*d
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>{escape(t)} | {SITE}</title><link rel="stylesheet" href="{p}css/style.css"><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>☠️</text></svg>"></head>'

def nv(d=0):
    p="../"*d;h=f"{p}" if d>0 else "index.html";ch=f"{p}contributors/" if d>0 else "contributors/";wh=f"{p}why/" if d>0 else "why/"
    return f'<nav class="nav-bar"><a href="{h}" class="nav-brand"><div class="nav-brand-icon">ADV</div><div class="nav-brand-text">Threat Actor Profiles</div></a><ul class="nav-links"><li><a href="{h}">Threat Actors</a></li><li><a href="{ch}">Contributors</a></li><li><a href="{wh}">Why This Project</a></li><li><a href="https://adversaryvillage.org" target="_blank">Adversary Village</a></li></ul><button class="nav-hamburger" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button></nav>'

def ft():
    return '<footer class="site-footer"><div class="footer-inner"><div class="footer-brand">Threat Actor Profiles</div><div class="footer-text">An open-source, community-driven threat actor profiles project by <a href="https://adversaryvillage.org" target="_blank" style="color:#604ca9;text-decoration:none;font-weight:600">Adversary Village</a>.</div><div style="color:var(--td);font-size:1.2rem;margin-top:.8rem">&copy; 2026 Adversary Village. All rights reserved.</div><ul class="footer-links"><li><a href="https://adversaryvillage.org" target="_blank">Adversary Village</a></li><li><a href="https://github.com/adversaryvillage" target="_blank">GitHub</a></li></ul></div></footer>'

def gidx(actors,sponsors=None):
    if sponsors is None: sponsors=[]
    countries=sorted(set(a.get('country','?') for a in actors))
    tt=sum(sum(len(t) for t in a.get('attack_techniques',{}).values()) for a in actors)
    pills="\n".join(f'<button class="filter-pill" data-filter="{escape(c.lower())}" data-filter-type="country">{escape(c)}</button>' for c in countries)
    cards=[]
    for a in actors:
        aid,name,flag,country,ttype=a['id'],a['name'],a.get('flag_emoji',''),a.get('country',''),a.get('threat_type','')
        al=a.get('aliases',[]);als=" / ".join(al[:3])+(f" +{len(al)-3}" if len(al)>3 else "")
        sd=f"{name} {' '.join(al)} {country} {ttype} {a.get('description','')}".lower()
        st=a.get('status','');sc='' if st.lower()=='active' else ' inactive'
        im=cimg_html(a,400,300,0)
        cards.append(f'<a href="{aid}/" class="actor-card" data-search="{escape(sd)}" data-country="{escape(country.lower())}" data-type="{escape(ttype.lower())}"><div class="card-image">{im}<span class="card-country-badge">{flag}</span><span class="card-type-badge {bc(ttype)}">{escape(ttype)}</span></div><div class="card-body"><div class="card-name">{escape(name)}</div><div class="card-aliases">{escape(als)}</div><div class="card-description">{escape(a.get("description",""))}</div><div class="card-meta"><span class="card-tag tag-country">{flag} {escape(country)}</span><span class="card-tag tag-active{sc}">● {escape(st)}</span></div></div><div class="card-footer"><span class="card-mitre-id">{escape(a.get("mitre_id",""))}</span><span class="card-arrow">View Profile</span></div></a>')
    # Sponsors section
    spon_html=''
    if sponsors:
        spon_cards=''
        tier_order={'Organizer':0,'Platinum':1,'Gold':2,'Silver':3,'Bronze':4,'Community':5}
        for s in sorted(sponsors,key=lambda x:tier_order.get(x.get('tier',''),99)):
            sname=s.get('name','');surl=s.get('url','#');stier=s.get('tier','')
            slogo=s.get('logo','');sdesc=s.get('description','')
            if slogo and os.path.isfile(os.path.join(SPONSORS_IMG,slogo)):
                logo_html=f'<img src="images/sponsors/{escape(slogo)}" alt="{escape(sname)}" style="max-height:60px;max-width:180px;object-fit:contain">'
            else:
                logo_html=f'<div style="font-family:var(--fh);font-size:1.8rem;font-weight:700;color:#fff">{escape(sname)}</div>'
            spon_cards+=f'<a href="{escape(surl)}" target="_blank" style="background:var(--bg-c);border:none;box-shadow:0 1px 6px rgba(0,0,0,0.25);border-radius:var(--r);padding:2rem;text-align:center;text-decoration:none;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1rem;transition:all var(--tr);width:100%">{logo_html}<div style="font-size:1.2rem;font-weight:700;letter-spacing:.15rem;text-transform:uppercase;color:var(--p)">{escape(stier)}</div><div style="font-size:1.3rem;color:var(--tm);line-height:1.5">{escape(sdesc[:80])}</div></a>'
        spon_html=f'<section style="max-width:1600px;margin:0 auto;padding:2rem 40px 5rem"><h2 style="font-family:var(--fh);font-size:2.4rem;font-weight:600;color:var(--p);text-align:center;margin-bottom:1rem">Sponsors & Supporters</h2><p style="text-align:center;color:var(--tm);font-size:1.5rem;margin-bottom:2.4rem">Organizations supporting the Threat Actors project and Adversary Village community.</p><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:1.6rem;justify-items:center">{spon_cards}</div></section>'
    html=f'''{hd(SITE)}<body>{nv(0)}<section class="hero"><div class="hero-grid"></div><div class="hero-label">☠ Community Threat Intelligence</div><h1><span class="highlight">Threat Actor</span> Profiles</h1><p class="hero-subtitle">An open-source encyclopedia of APT profiles, attack path diagrams, emulation plans, and detection engineering by Adversary Village.</p><div class="hero-stats"><div class="hero-stat"><div class="hero-stat-value">{len(actors)}</div><div class="hero-stat-label">Threat Actors</div></div><div class="hero-stat"><div class="hero-stat-value">{tt}</div><div class="hero-stat-label">Techniques</div></div><div class="hero-stat"><div class="hero-stat-value">{len(countries)}</div><div class="hero-stat-label">Nations</div></div></div></section><div class="filter-bar"><div class="search-box"><input type="text" id="actor-search" placeholder="Search threat actors, aliases, techniques..."></div><div class="filter-pills"><button class="filter-pill active" data-filter="all">All</button>{pills}<button class="filter-pill" data-filter="nation-state" data-filter-type="type">Nation-State</button><button class="filter-pill" data-filter="criminal" data-filter-type="type">Cybercriminal</button></div></div><section class="cards-section"><div class="cards-grid">{chr(10).join(cards)}</div></section>{spon_html}{ft()}<script src="js/main.js"></script></body></html>'''
    with open(os.path.join(OUT,'index.html'),'w') as f: f.write(fmt_html(html))
    print("  ✓ index.html")

def gact(a):
    # Get JSON file modification time for last-updated
    json_path=os.path.join(DATA,f"{a['id']}.json")
    if os.path.isfile(json_path):
        import time as _tm
        mtime=os.path.getmtime(json_path)
        last_updated=_tm.strftime('%B %d, %Y',_tm.localtime(mtime))
    else:
        last_updated='Unknown'
    aid,name,flag,country,mid=a['id'],a['name'],a.get('flag_emoji',''),a.get('country',''),a.get('mitre_id','')
    st=a.get('status','');sc='' if st.lower()=='active' else ' inactive'
    tc=sum(len(t) for t in a.get('attack_techniques',{}).values())
    tac=sum(1 for t in a.get('attack_techniques',{}).values() if t)
    him=cimg_html(a,800,500,1)
    ac=''.join(f'<span class="chip">{escape(x)}</span>' for x in a.get('aliases',[]))
    toc=''.join(f'<span class="chip chip-purple">{escape(x)}</span>' for x in a.get('tools',[]))
    sec=''.join(f'<span class="chip chip-cyan">{escape(x)}</span>' for x in a.get('target_sectors',[]))
    tcc=", ".join(a.get('target_countries',[]))
    ind_chips=''.join(f'<span class="chip chip-orange">{escape(x)}</span>' for x in a.get('target_industries',a.get('target_sectors',[])))
    flag_chips=''.join(f'<span class="chip" style="font-size:1.4rem">{escape(c.get("flag",""))} {escape(c.get("country",""))}</span>' for c in a.get('target_country_flags',[]))
    if not flag_chips: flag_chips=''.join(f'<span class="chip">{escape(x)}</span>' for x in a.get('target_countries',[]))
    refs=''.join(f'<li class="ref-item"><a href="{escape(r.get("url","#"))}" target="_blank">{escape(r.get("title",""))}</a></li>' for r in a.get('references',[]))
    nu=f"https://mitre-attack.github.io/attack-navigator/#layerURL=https%3A%2F%2Fattack.mitre.org%2Fgroups%2F{mid}%2F{mid}-enterprise-layer.json"
    af=a.get('attack_flow',{});afs=afsvg(af.get('steps',[]),af.get('campaign',''))
    dm=a.get('diamond_model',{})
    dia=diamond_svg(dm)
    if not dia:
        dia=f'<div class="diamond-grid"><div class="diamond-cell"><div class="diamond-cell-title">Adversary</div><div class="diamond-cell-content">{escape(dm.get("adversary","-"))}</div></div><div class="diamond-cell"><div class="diamond-cell-title">Infrastructure</div><div class="diamond-cell-content">{escape(dm.get("infrastructure","-"))}</div></div><div class="diamond-cell"><div class="diamond-cell-title">Capability</div><div class="diamond-cell-content">{escape(dm.get("capability","-"))}</div></div><div class="diamond-cell"><div class="diamond-cell-title">Victim</div><div class="diamond-cell-content">{escape(dm.get("victim","-"))}</div></div></div>'
    # Malware detail cards with tool URLs from JSON
    tools=a.get('tools',[])
    tool_urls={t.get('name','').lower():t for t in a.get('tool_urls',[])}
    malware_cards=''
    if tools:
        malware_cards='<div class="related-grid">'
        for t2 in tools[:12]:
            tu=tool_urls.get(t2.lower(),{})
            tu_link=f'<a href="{escape(tu.get("url","#"))}" target="_blank" style="display:inline-block;margin-top:.6rem;font-size:1.2rem;font-weight:600;color:var(--p)">{escape(tu.get("type","View Details"))}</a>' if tu.get('url') else f'<a href="https://attack.mitre.org/software/" target="_blank" style="display:inline-block;margin-top:.6rem;font-size:1.2rem;font-weight:600;color:var(--td)">ATT&CK Software</a>'
            malware_cards+=f'<div class="related-card"><div class="related-card-name">{escape(t2)}</div><div class="related-card-rel">{escape(tu.get("type","Malware / Tool"))}</div>{tu_link}</div>'
        # Also add tool_urls that aren't already in the tools list
        for tu in a.get('tool_urls',[]):
            if tu.get('name','').lower() not in [t.lower() for t in tools]:
                malware_cards+=f'<div class="related-card"><div class="related-card-name">{escape(tu.get("name",""))}</div><div class="related-card-rel">{escape(tu.get("type","Public Tool"))}</div><a href="{escape(tu.get("url","#"))}" target="_blank" style="display:inline-block;margin-top:.6rem;font-size:1.2rem;font-weight:600;color:var(--p)">Source / Analysis</a></div>'
        malware_cards+='</div>'
    cves=a.get('cves',[])
    cvh='<table class="cve-table"><thead><tr><th>CVE</th><th>Year</th><th>Description</th></tr></thead><tbody>'+''.join(f'<tr><td class="cve-id"><a href="https://nvd.nist.gov/vuln/detail/{escape(c["id"])}" target="_blank">{escape(c["id"])}</a></td><td>{escape(c.get("year",""))}</td><td>{escape(c.get("desc",""))}</td></tr>' for c in cves)+'</tbody></table>' if cves else '<p style="color:var(--tm)">No CVE data.</p>'
    # IOC Sources from JSON data - real per-actor URLs
    ioc_list = a.get('ioc_sources', [])
    if ioc_list:
        ioc_src = '<div class="detail-grid">' + ''.join(f'<div class="detect-block"><div class="detect-block-title">{escape(s.get("name",""))}</div><div class="detect-block-content">{escape(s.get("desc",""))}</div><div style="font-size:1.1rem;color:var(--td);word-break:break-all;margin-top:.4rem">{escape(s.get("url",""))}</div><a href="{escape(s.get("url","#"))}" target="_blank" style="display:inline-block;margin-top:.6rem;font-size:1.3rem;font-weight:600;color:var(--p)">View IOC Source</a></div>' for s in ioc_list) + '</div>'
    else:
        ioc_src = f'<p style="color:var(--tm)">No IOC sources. Add <code>ioc_sources</code> array to the JSON file.</p>'
    det=a.get('detection',[])

    def _rdet(d):
        c2=d.get('content','');t2=d.get('title','');u2=d.get('url','')
        lk='<div style="margin-top:1rem;display:flex;gap:1.2rem;flex-wrap:wrap">'
        if u2:
            lk+=f'<a href="{escape(u2)}" target="_blank" style="font-size:1.3rem;font-weight:700;color:var(--p)">View Detection Rule / Guide</a>'
        lk+='</div>'
        return f'<div class="detect-block"><div class="detect-block-title">{escape(t2)}</div><div class="detect-block-content" style="font-size:1.5rem;line-height:1.7">{escape(c2)}</div>{lk}</div>'
    deh=''.join(_rdet(d) for d in det) if det else '<p style="color:var(--tm)">No detection data.</p>'
    rel=a.get('related_actors',[])
    def _rcard(r):
        rn=r.get('name','')
        return f'<div class="related-card"><div class="related-card-name">{escape(rn)}</div><div class="related-card-rel">{escape(r.get("relationship",""))}</div><div class="related-card-desc">{escape(r.get("desc",""))}</div><div style="margin-top:.8rem;display:flex;gap:1rem"><a href="https://attack.mitre.org/groups/" target="_blank" style="font-size:1.1rem;font-weight:600;color:var(--p)">MITRE ATT&CK</a><a href="https://www.mandiant.com/resources/blog?search={escape(rn.replace(" ","+"))}" target="_blank" style="font-size:1.1rem;font-weight:600;color:var(--p)">Mandiant</a></div></div>'
    reh='<div class="related-grid">'+''.join(_rcard(r) for r in rel)+'</div>' if rel else ''
    dfs=a.get('defense_recommendations',[])
    _mmap={'mfa':'M1032','fido':'M1032','authentication':'M1032','segment':'M1030','vlan':'M1030','patch':'M1051','update':'M1051','macro':'M1042','office':'M1042','edr':'M1049','endpoint':'M1049','powershell':'M1045','script':'M1045','allowlist':'M1038','applocker':'M1038','wdac':'M1038','backup':'M1053','train':'M1017','awareness':'M1017','dns':'M1031','filter':'M1037','firewall':'M1037','egress':'M1037','privilege':'M1026','admin':'M1026','paw':'M1026'}
    def _rdef(i,d):
        if isinstance(d,dict):
            txt=d.get('text','');src=d.get('source','');url=d.get('url','')
            srclink=f'<a href="{escape(url)}" target="_blank" style="font:600 1.3rem Nunito Sans;color:#604ca9;display:inline-block;margin-top:.6rem">{escape(src)}</a>' if url else f'<span style="font:600 1.2rem Nunito Sans;color:var(--td);margin-top:.4rem;display:inline-block">{escape(src)}</span>'
            return f'<div class="detect-block" style="padding:1.4rem"><div style="font:600 1.5rem Nunito Sans;color:var(--t2);line-height:1.7;margin-bottom:.4rem">{escape(txt)}</div>{srclink}</div>'
        else:
            return f'<div class="detect-block" style="padding:1.4rem"><div style="font:600 1.5rem Nunito Sans;color:var(--t2);line-height:1.7">{escape(str(d))}</div></div>'
    dfh=f'<div class="detail-grid">{"".join(_rdef(i,d) for i,d in enumerate(dfs))}</div>' if dfs else ''
    eps=a.get('emulation_plans',[])
    def _epr(p):
        return f'<tr><td class="plan-name">{escape(p.get("name",""))}</td><td class="plan-source">{escape(p.get("source",""))}</td><td style="color:var(--td);font-size:1.2rem">{escape(p.get("type",""))}</td><td>{escape(p.get("desc",""))}</td><td><a href="{escape(p.get("url","#"))}" target="_blank" style="color:#604ca9;font-weight:600">Open</a></td></tr>'
    eph='<table class="emulation-table"><thead><tr><th>Plan</th><th>Source</th><th>Type</th><th>Description</th><th>Link</th></tr></thead><tbody>'+''.join(_epr(p) for p in eps)+'</tbody></table>' if eps else '<p style="color:var(--tm)">No emulation plans.</p>'
    camps=a.get('notable_campaigns',[])
    cah='<div class="campaign-timeline">'+''.join(f'<div class="campaign-item"><div class="campaign-year">{escape(c.get("year",""))}</div><div class="campaign-name">{escape(c.get("name",""))}</div><div class="campaign-desc">{escape(c.get("description",""))}</div></div>' for c in sorted(camps,key=lambda x:x.get('year',''),reverse=True))+'</div>'
    # Attribution Confidence
    ac_data=a.get('attribution_confidence',{})
    ac_level=ac_data.get('level','Unknown')
    ac_color={"High":"#4ecca3","Medium":"#ffd166","Low":"#f4845f"}.get(ac_level,"#a8b2c1")
    ac_evidence=ac_data.get('evidence',[])
    def _ac_ev(e):
        if isinstance(e,dict):
            return f'<div style="padding:1.2rem;background:rgba(255,255,255,0.02);border:none;box-shadow:0 1px 6px rgba(0,0,0,0.25);border-radius:4px"><div style="font-size:1.4rem;color:var(--t2);line-height:1.6">{escape(e.get("text",""))}</div><a href="{escape(e.get("url","#"))}" target="_blank" style="font:600 1.2rem Nunito Sans;color:#604ca9;margin-top:.4rem;display:inline-block">{escape(e.get("url","")[:60])}</a></div>'
        return f'<div style="padding:1.2rem;background:rgba(255,255,255,0.02);border:none;box-shadow:0 1px 6px rgba(0,0,0,0.25);border-radius:4px;font-size:1.4rem;color:var(--t2);line-height:1.6">{escape(str(e))}</div>'
    ac_ev_cards=''.join(_ac_ev(e) for e in ac_evidence)
    ac_html=f'<div class="grid-2col-wide" style="grid-template-columns:180px 1fr"><div style="display:flex;flex-direction:column;align-items:center;gap:1rem"><div style="width:140px;height:140px;border-radius:50%;background:{ac_color}12;border:3px solid {ac_color};display:flex;flex-direction:column;align-items:center;justify-content:center"><div style="font:700 3.2rem Chivo;color:{ac_color}">{escape(ac_level)}</div></div><div style="font:700 1.2rem Nunito Sans;color:var(--td);letter-spacing:1px;text-transform:uppercase;text-align:center">Attribution<br>Confidence</div></div><div><div style="font:600 1.6rem Chivo;color:#fff;margin-bottom:1.2rem">Evidence Supporting Attribution</div><div style="display:grid;grid-template-columns:1fr 1fr;gap:.8rem">{ac_ev_cards}</div></div></div>'

    # Legal Actions
    la=a.get('legal_actions',[])
    la_html='<div class="campaign-timeline">'+''.join(f'<div class="campaign-item"><div class="campaign-year">{escape(l.get("date",""))}</div><div class="campaign-name">{escape(l.get("title",""))}</div><div style="margin-top:.4rem"><span class="la-type">{escape(l.get("type",""))}</span></div><a href="{escape(l.get("url","#"))}" target="_blank" style="display:inline-block;margin-top:.6rem;font:600 1.3rem Nunito Sans;color:var(--p)">{escape(l.get("url",""))}</a></div>' for l in la)+'</div>' if la else '<p style="color:var(--tm)">No documented legal actions.</p>'

    # Threat Assessment
    ta=a.get('threat_assessment',{})
    ta_cap=ta.get('capability',0);ta_int=ta.get('intent',0);ta_tgt=ta.get('targeting',0);ta_ovr=ta.get('overall','Unknown');ta_sum=ta.get('summary','')
    ta_color={"Critical":"#E91E63","High":"#f4845f","Moderate":"#ffd166","Low":"#4ecca3"}.get(ta_ovr,"#a8b2c1")
    def _bar(label,val,color):
        pct=val*10
        return f'<div style="margin-bottom:1rem"><div style="display:flex;justify-content:space-between;margin-bottom:.4rem"><span style="font:600 1.3rem Nunito Sans;color:var(--t2)">{label}</span><span style="font:700 1.3rem Chivo;color:{color}">{val}/10</span></div><div style="height:8px;background:rgba(255,255,255,0.05);border-radius:4px;overflow:hidden"><div style="height:100%;width:{pct}%;background:{color};border-radius:4px;transition:width 0.5s"></div></div></div>'
    ta_html=f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:2rem;align-items:start"><div>{_bar("Capability",ta_cap,"#604ca9")}{_bar("Intent",ta_int,"#E91E63")}{_bar("Targeting",ta_tgt,"#ffd166")}<div style="margin-top:1.6rem;padding:1.4rem;background:{ta_color}10;border:1px solid {ta_color}30;border-radius:6px;text-align:center"><div style="font:700 2rem Chivo;color:{ta_color}">{escape(ta_ovr)}</div><div style="font:400 1.1rem Nunito Sans;color:var(--td);margin-top:.2rem">Overall Threat Level</div></div></div><div style="font-size:1.5rem;color:var(--t2);line-height:1.7">{escape(ta_sum)}</div></div>'

    # Kill Chain
    kc=a.get('kill_chain',[])
    kc_html='<div style="display:flex;flex-direction:column;gap:.8rem">'+''.join(f'<div style="display:grid;grid-template-columns:180px 1fr;gap:1rem;padding:1rem 1.4rem;background:rgba(255,255,255,0.02);border:none;box-shadow:0 1px 6px rgba(0,0,0,0.25);border-radius:4px;border-left:3px solid #604ca9"><div style="font:700 1.3rem Chivo;color:var(--p)">{escape(k.get("phase",""))}</div><div style="font:400 1.4rem Nunito Sans;color:var(--t2);line-height:1.6">{escape(k.get("mapping",""))}</div></div>' for k in kc)+'</div>' if kc else ''

    # Activity Timeline
    camps_all=a.get('notable_campaigns',[])
    if camps_all:
        sorted_camps=sorted(camps_all,key=lambda x:x.get('year',''))
        tl_bars=''
        for c3 in sorted_camps:
            tl_bars+=f'<div style="display:inline-flex;flex-direction:column;align-items:center;min-width:80px;padding:0 8px"><div style="width:16px;height:16px;background:#604ca9;border-radius:50%;border:2px solid #7b68c4;position:relative;z-index:2"></div><div style="font:700 1.2rem Chivo;color:#fff;margin-top:.6rem;text-align:center">{escape(c3.get("year",""))}</div><div style="font:400 1.1rem Nunito Sans;color:var(--td);margin-top:.2rem;text-align:center;max-width:120px">{escape(c3.get("name","")[:25])}</div></div>'
        timeline_html=f'<div style="position:relative;overflow-x:auto;padding:2rem 1rem"><div style="display:flex;align-items:flex-start;gap:0;position:relative;min-width:max-content"><div style="position:absolute;top:7px;left:20px;right:20px;height:2px;background:rgba(96,76,169,0.3)"></div>{tl_bars}</div></div>'
    else:
        timeline_html='<p style="color:var(--tm)">No campaign timeline data.</p>'

    # Recent News
    news=a.get('recent_news',[])
    news_html='<div style="display:flex;flex-direction:column;gap:.8rem">'+''.join(f'<div class="news-row"><div style="font:700 1.3rem Chivo;color:var(--p)">{escape(n.get("date",""))}</div><div><div style="font:600 1.5rem Nunito Sans;color:#fff;margin-bottom:.4rem">{escape(n.get("title",""))}</div><a href="{escape(n.get("url","#"))}" target="_blank" style="font:400 1.2rem Nunito Sans;color:var(--p);word-break:break-all">{escape(n.get("url",""))}</a></div></div>' for n in news)+'</div>' if news else '<p style="color:var(--tm)">No recent news entries.</p>'

    # Data Sources & Page Contributors (footer sections)
    dsrc=a.get('data_sources',[])
    pcon=a.get('page_contributors',[])
    footer_meta=''

    # Data Sources cards
    dsrc=a.get('data_sources',[])
    dsrc_cards=''.join(f'<li><div class="ref-title">{escape(s.get("name","") if isinstance(s,dict) else str(s))}</div><a href="{escape(s.get("url","#") if isinstance(s,dict) else "#")}" target="_blank">{escape(s.get("url","") if isinstance(s,dict) else "")}</a></li>' for s in dsrc)
    # Page Contributors cards with social links
    pcon=a.get('page_contributors',[])
    pcon_cards=''
    for pc in pcon:
        if isinstance(pc, dict):
            pcn=pc.get('name','');pcgh=pc.get('github','');pctw=pc.get('twitter','');pcli=pc.get('linkedin','')
            slinks=''
            if pcgh: slinks+=f'<a href="{escape(pcgh)}" target="_blank" style="font:600 1.2rem Nunito Sans;color:#604ca9">GitHub</a> '
            if pctw: slinks+=f'<a href="{escape(pctw)}" target="_blank" style="font:600 1.2rem Nunito Sans;color:#604ca9">Twitter</a> '
            if pcli: slinks+=f'<a href="{escape(pcli)}" target="_blank" style="font:600 1.2rem Nunito Sans;color:#604ca9">LinkedIn</a>'
            pcon_cards+=f'<div class="contrib-card"><div class="contrib-name">{escape(pcn)}</div><div style="display:flex;gap:1.2rem;flex-wrap:wrap">{slinks}</div></div>'
        else:
            pcon_cards+=f'<div style="padding:1.4rem;background:rgba(255,255,255,0.02);border:none;box-shadow:0 1px 6px rgba(0,0,0,0.25);border-radius:6px"><div style="font:600 1.5rem Chivo;color:#fff">{escape(str(pc))}</div></div>'

        # TTP Emulation Commands
    ttps=a.get('ttp_commands',[])
    ttp_html=''
    if ttps:
        ttp_html='<div style="overflow-x:auto"><table class="emulation-table" style="min-width:900px"><thead><tr><th>TID</th><th>Technique</th><th>Tactic</th><th>Tool</th><th>Command</th><th>Platform</th><th>Source</th></tr></thead><tbody>'
        for t in ttps:
            cmd=escape(t.get('command',''))
            ttp_html+=f'<tr><td style="font:700 1.3rem Nunito Sans;color:var(--p);white-space:nowrap">{escape(t.get("tid",""))}</td><td style="font:600 1.3rem Chivo;color:#fff;min-width:140px">{escape(t.get("name",""))}</td><td style="color:var(--td);font-size:1.2rem">{escape(t.get("tactic",""))}</td><td style="font:600 1.2rem Nunito Sans;color:var(--or)">{escape(t.get("tool",""))}</td><td><code style="font:400 1.2rem Consolas,monospace;color:var(--gn);background:rgba(78,204,163,0.06);padding:.3rem .6rem;border-radius:3px;display:block;white-space:pre-wrap;word-break:break-all;max-width:340px">{cmd}</code><div style="font:400 1.1rem Nunito Sans;color:var(--td);margin-top:.3rem">{escape(t.get("note",""))}</div></td><td style="font-size:1.2rem;color:var(--td)">{escape(t.get("platform",""))}</td><td><a href="{escape(t.get("url","#"))}" target="_blank" style="font:600 1.2rem Nunito Sans;color:#604ca9">Source</a></td></tr>'
        ttp_html+='</tbody></table></div>'

    # Search bar for actor page
    search_html=f'<div id="page-search" class="page-search"><input type="text" id="page-search-input" placeholder="Search this page..." ></div><script>document.getElementById("page-search-input").addEventListener("input",function(e){{var q=e.target.value.toLowerCase();document.querySelectorAll(".content-section,.detect-block").forEach(function(el){{if(!q){{el.style.display="";return}}el.style.display=el.textContent.toLowerCase().includes(q)?"":"none"}})}});</'+'script>'

    # Last updated timestamp
    timestamp_html=f'<div style="font:400 1.2rem Nunito Sans;color:var(--td);margin-top:.4rem">Last updated: {last_updated}</div>'

            # References from JSON only - real verified URLs
    arefs = a.get('references', [])
    # Merge IOC sources into references
    for src in a.get('ioc_sources', []):
        arefs.append({"title": src.get("name",""), "url": src.get("url","")})
    if not arefs:
        arefs = [{"title":f"MITRE ATT&CK {name} ({mid})","url":f"https://attack.mitre.org/groups/{mid}/"}]
    # Deduplicate by URL
    seen=set(); deduped=[]
    for r in arefs:
        u=r.get('url','')
        if u and u not in seen:
            deduped.append(r); seen.add(u)
    arefs=deduped
    refs=''.join(f'<li><div class="ref-title">{escape(r.get("title",""))}</div><a href="{escape(r.get("url","#"))}" target="_blank">{escape(r.get("url",""))}</a></li>' for r in arefs)
    # Output: docs/{aid}/index.html for clean URLs
    adir=os.path.join(OUT,aid);os.makedirs(adir,exist_ok=True)
    html=f'''{hd(name,1)}<body class="actor-page">{nv(1)}<div class="breadcrumb"><a href="../">← Threat Actors</a> / {escape(name)} {timestamp_html}</div>
<div class="actor-hero-split"><div class="actor-hero-art">{him}<div class="art-overlay"><div class="art-name">{escape(name)}</div><div class="art-sub">{escape(a.get('attribution',''))}</div></div></div>
<div class="actor-hero-info"><div class="info-badges"><span class="card-tag tag-country">{flag} {escape(country)}</span><span class="card-type-badge {bc(a.get('threat_type',''))}">{escape(a.get('threat_type',''))}</span><span class="card-tag tag-active{sc}">● {escape(st)}</span><span class="card-tag" style="background:rgba(255,255,255,0.04);color:var(--td);border:none;box-shadow:0 1px 6px rgba(0,0,0,0.25)">{escape(mid)}</span></div>
<div class="info-card"><div class="info-card-title">Key Intelligence</div><div class="info-grid"><div class="info-field"><div class="info-label">MITRE ID</div><div class="info-value"><a href="https://attack.mitre.org/groups/{escape(mid)}" target="_blank">{escape(mid)}</a></div></div><div class="info-field"><div class="info-label">Country</div><div class="info-value">{flag} {escape(country)}</div></div><div class="info-field"><div class="info-label">Motivation</div><div class="info-value">{escape(a.get('motivation',''))}</div></div><div class="info-field"><div class="info-label">Active Since</div><div class="info-value">{escape(a.get('first_seen',''))}</div></div><div class="info-field"><div class="info-label">Last Seen</div><div class="info-value">{escape(a.get('last_seen',''))}</div></div><div class="info-field"><div class="info-label">Techniques</div><div class="info-value">{tc} across {tac} tactics</div></div><div class="info-field info-full"><div class="info-label">Attribution</div><div class="info-value">{escape(a.get('attribution',''))}</div></div><div class="info-field info-full"><div class="info-label">Also Known As</div><div class="chip-list">{ac}</div></div></div></div>
<div class="info-card" style="flex:0"><div class="info-card-title">Target Profile</div><div class="info-grid"><div class="info-field info-full"><div class="info-label">Targeted Industries</div><div class="chip-list">{ind_chips}</div></div><div class="info-field info-full"><div class="info-label">Targeted Countries</div><div class="chip-list">{flag_chips}</div></div></div></div></div></div>
{search_html}<div class="actor-below"><div class="actor-below-grid">
<div class="content-section"><h2 class="section-title">Overview</h2><div class="description-text">{escape(a.get('description',''))}</div></div>
<div class="content-section"><h2 class="section-title">Tools & Malware</h2><div class="chip-list">{toc}</div></div>
<div class="content-section actor-below-full"><h2 class="section-title">Malware & Tool Details</h2><p style="color:var(--tm);font-size:1.4rem;margin-bottom:1.4rem">Arsenal attributed to {escape(name)}.</p>{malware_cards}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Attack Path {escape(af.get('campaign',''))}</h2><p style="color:var(--tm);font-size:1.4rem;margin-bottom:1.6rem">Following <a href="https://center-for-threat-informed-defense.github.io/attack-flow/" target="_blank">MITRE ATT&CK Flow</a> methodology.</p>{afs}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Diamond Model</h2>{dia}</div>
<div class="content-section actor-below-full"><h2 class="section-title">ATT&CK Navigator</h2><p style="color:var(--tm);font-size:1.4rem;margin-bottom:1.6rem">Interactive MITRE ATT&CK Navigator layer for {escape(name)} ({escape(mid)}).</p><div style="position:relative"><div id="nav-skel-{aid}" class="nav-skel"><div class="nav-spinner"></div><div style="font-size:1.3rem;color:var(--td)">Loading ATT&CK Navigator...</div></div><iframe class="navigator-frame" src="{nu}" title="ATT&CK Navigator" loading="lazy" sandbox="allow-scripts allow-same-origin allow-popups" onload="var s=document.getElementById('nav-skel-'+'{aid}');if(s)s.style.display='none'"></iframe></div><a href="{nu}" target="_blank" class="navigator-link">Open Full Navigator</a></div>
<div class="content-section"><h2 class="section-title">Known CVEs Exploited</h2>{cvh}</div>
<div class="content-section"><h2 class="section-title">Notable Campaigns</h2>{cah}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Detection Engineering</h2>{deh}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Related Threat Actors</h2><p style="color:var(--tm);font-size:1.3rem;margin-bottom:1rem">Documented in MITRE ATT&CK, vendor intelligence, and government advisories.</p>{reh}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Defense Recommendations</h2><p style="color:var(--tm);font-size:1.3rem;margin-bottom:1rem">Mitigations with MITRE ATT&CK IDs. Click badges for implementation guidance.</p>{dfh}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Attribution Confidence</h2>{ac_html}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Threat Assessment</h2>{ta_html}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Legal Actions & Sanctions</h2>{la_html}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Recent Reporting</h2>{news_html}</div>
<div class="content-section actor-below-full"><h2 class="section-title">Emulation Plans & Guidance</h2>{eph}</div>
<div class="content-section actor-below-full"><h2 class="section-title">References & Intelligence Sources</h2><ul class="ref-list-2col">{refs}{dsrc_cards}</ul></div>
<div class="content-section actor-below-full"><h2 class="section-title">Page Contributors</h2><div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:1.2rem">{pcon_cards}</div></div>
</div></div>{ft()}<script src="../js/main.js"></script></body></html>'''
    with open(os.path.join(adir,'index.html'),'w') as f: f.write(fmt_html(html))
    print(f"  ✓ {aid}/index.html")

def main():
    print(f"\n{'='*60}\n  {SITE} Generator v5\n  Data: data/actors/*.json\n  Images: data/actors/images/\n  URLs: /{'{actor_id}'}/ (clean paths)\n{'='*60}\n")
    os.makedirs(OUT,exist_ok=True);cpimg()
    copy_dir_images(CONTRIB_IMG,CONTRIB_IMG_OUT)
    copy_dir_images(SPONSORS_IMG,SPONSORS_IMG_OUT)
    actors=load()
    contributors=load_json(CONTRIB_FILE)
    sponsors=load_json(SPONSORS_FILE)
    print(f"  {len(actors)} profiles, {len(contributors)} contributors, {len(sponsors)} sponsors\n")
    for a in actors:
        im=fimg(a['id'])
        print(f"    {'📷' if im else '🎨'} {a['id']}: {'custom '+im if im else 'SVG fallback'}")
    print(f"\n  Generating...")
    gidx(actors,sponsors)
    for a in actors: gact(a)
    gen_why()
    gen_contributors(contributors)
    print(f"\n  ✅ {len(actors)+3} pages\n")
    print("  URL structure:")
    print("    actors.adversaryvillage.org/              index.html")
    print("    actors.adversaryvillage.org/apt28/         apt28/index.html")
    print("    actors.adversaryvillage.org/why/            why/index.html")
    print("    actors.adversaryvillage.org/contributors/  contributors/index.html\n")


def gen_why():
    wdir=os.path.join(OUT,'why');os.makedirs(wdir,exist_ok=True)
    c='<section style="padding:150px 40px 60px;max-width:900px;margin:0 auto">'
    c+='<div style="font:700 1.4rem var(--fb);letter-spacing:.4rem;text-transform:uppercase;color:var(--p);margin-bottom:1.6rem">About</div>'
    c+='<h1 style="font:600 4.5rem var(--fh);color:#fff;margin-bottom:2.4rem;line-height:1.2">Why This Project</h1>'
    c+='<div style="font-size:1.8rem;line-height:1.9;color:var(--t2)">'

    c+='<h2 style="font:600 2.8rem var(--fh);color:#fff;margin:0 0 1.6rem">How it started</h2>'
    c+='<p style="margin-bottom:2rem">This project began when I (Abhijith) was creating threat actor artwork and adversary emulation plans for a few APT groups as part of our work at <a href="https://adversaryvillage.org" target="_blank" style="color:#604ca9;font-weight:600">Adversary Village</a>. We needed quality visuals and structured data for conference talks, training sessions, and community content. I put together a few actor profiles with custom artwork, mapped their TTPs, wrote up emulation guidance, and quickly realized — there was nothing like this that existed as a single, open, reusable resource.</p>'

    c+='<p style="margin-bottom:2rem">There are plenty of places to read about threat actors. MITRE ATT&CK provides the framework. CISA publishes advisories. Vendors release reports. Researchers share IOCs across dozens of platforms. But nowhere could you get the full picture in one page — who they are, what tools they use, how they attack, how to emulate them, how to detect them, and how to defend against them. All sourced, all linked, all free.</p>'

    c+='<p style="margin-bottom:2rem">That gap is what <strong style="color:#fff">Threat Actor Profiles</strong> fills. And it is open to everyone.</p>'

    c+='<h2 style="font:600 2.8rem var(--fh);color:#fff;margin:3rem 0 1.6rem">Free profiles for the community</h2>'
    c+='<p style="margin-bottom:2rem">Every profile on this site — the artwork, the data, the interactive diagrams — is free for anyone to use in their projects, conference presentations, training workshops, university courses, or research. Building a talk on APT29 for a conference? The profile page is here. Running a purple team training on ransomware actors? FIN7\'s full attack chain breakdown is here. No paywalls, no vendor lock-in, no login required.</p>'

    c+='<p style="margin-bottom:2rem">The threat intelligence community produces incredible research, but it is scattered across hundreds of vendor blogs, government advisories, and academic papers. This project brings it together into structured, consistent, actionable profiles that anyone can use and anyone can improve.</p>'

    c+='<h2 style="font:600 2.8rem var(--fh);color:#fff;margin:3rem 0 1.6rem">A practical guide to emulating threat actors</h2>'
    c+='<p style="margin-bottom:2rem">The second goal is equally important. We want this to be the go-to resource for understanding <em>how</em> to emulate these threat actors in your own environment. Every profile includes an Emulation Plans & Guidance section with direct links to step-by-step emulation walkthroughs, open-source adversary simulation repos with full attack chains you can run in a lab, MITRE CTID emulation plans with Caldera abilities and payloads, and blog posts from practitioners who have actually built and executed these emulations.</p>'

    c+='<p style="margin-bottom:2rem">Whether you are a red teamer building an adversary emulation exercise, a purple team operator validating your detections, a SOC analyst studying how a specific actor operates, or a student learning offensive security — these profiles give you everything you need to go from reading about a threat actor to actually replicating their behavior in a controlled environment.</p>'

    c+='<h2 style="font:600 2.8rem var(--fh);color:#fff;margin:3rem 0 1.6rem">Sourced and verified</h2>'
    c+='<p style="margin-bottom:2rem">Every claim on every profile is sourced. Defense recommendations cite who recommends them — CISA, NIST, NSA, Microsoft — with URLs to the actual documents. Detection rules link to real Sigma YAML files on GitHub. Emulation plans link to repos you can clone and run. Attribution evidence cites DOJ indictments and government advisories. If something does not have a source, it does not belong here.</p>'

    c+='<h2 style="font:600 2.8rem var(--fh);color:#fff;margin:3rem 0 1.6rem">Contributors welcome</h2>'
    c+='<p style="margin-bottom:1.4rem">This is a community project and we need people who can help. You can contribute by adding new threat actor profiles, creating actor artwork, writing emulation guides, adding detection content like Sigma rules and KQL queries, improving existing profiles with new references and campaigns, or fixing broken URLs.</p>'

    c+='<p style="margin-bottom:2rem">No contribution is too small. Even fixing a single broken URL or adding one missing CVE helps the entire community.</p>'

    c+='<p style="margin-bottom:2rem">The entire project is data-driven. Every actor page is generated from a single JSON file. You do not need to know Python or HTML. Edit the JSON, submit a pull request, and the maintainers review and merge. Check the <a href="https://github.com/adversaryvillage/threat-actor-profiles" target="_blank" style="color:#604ca9;font-weight:600">README on GitHub</a> for the full contribution guide.</p>'

    c+='<a href="https://github.com/adversaryvillage" target="_blank" style="display:inline-block;padding:1.4rem 3.2rem;background:var(--p);color:#fff;border-radius:var(--r);font:700 1.4rem var(--fb);letter-spacing:.15rem;text-transform:uppercase;text-decoration:none;margin-top:1rem">Contribute on GitHub</a>'

    c+='</div></section>'
    html=hd('Why This Project',1)+'<body>'+nv(1)+c+ft()+'<script src="../js/main.js"></script></body></html>'
    with open(os.path.join(wdir,'index.html'),'w') as f2: f2.write(fmt_html(html))
    print("  ✓ why/index.html")

def gen_contributors(contributors):
    """Generate contributors page at /contributors/index.html."""
    cdir=os.path.join(OUT,'contributors');os.makedirs(cdir,exist_ok=True)
    # Load sponsors for supporters section
    import json as _cj
    spon_list=[]
    if os.path.isfile(SPONSORS_FILE):
        with open(SPONSORS_FILE,'r') as sf: spon_list=_cj.load(sf)
    spon_cards=''.join(f'<a href="{escape(s.get("url","#"))}" target="_blank" style="display:block;padding:2rem;background:#fff;border:1px solid #e0e0e0;border-radius:8px;text-decoration:none;text-align:center;transition:all 0.3s"><div style="font-family:var(--fh);font-size:1.8rem;font-weight:700;color:var(--p);margin-bottom:.6rem">{escape(s.get("name",""))}</div><div style="font-size:1.3rem;color:#666;line-height:1.5">{escape(s.get("desc",""))}</div></a>' for s in spon_list)
    cards=''
    for c in contributors:
        name=c.get('name','');role=c.get('role','');bio=c.get('bio','')
        photo=c.get('photo','')
        gh=c.get('github','');tw=c.get('twitter','');li=c.get('linkedin','');ws=c.get('website','')
        # Photo: check if exists, else use initials
        if photo and os.path.isfile(os.path.join(CONTRIB_IMG,photo)):
            img_html=f'<img src="../images/contributors/{escape(photo)}" alt="{escape(name)}" style="width:100%;height:100%;object-fit:cover">'
        else:
            initials=''.join(w[0].upper() for w in name.split()[:2]) if name else '?'
            img_html=f'<div style="width:100%;height:100%;background:#f0f0f5;display:flex;align-items:center;justify-content:center;font-family:var(--fh);font-size:4rem;font-weight:900;color:var(--p)">{escape(initials)}</div>'
        # Social links
        socials=''
        if gh: socials+=f'<a href="{escape(gh)}" target="_blank" style="color:var(--p);font-size:1.4rem;font-weight:600">GitHub</a>'
        if tw: socials+=f'<a href="{escape(tw)}" target="_blank" style="color:var(--p);font-size:1.4rem;font-weight:600">X / Twitter</a>'
        if li: socials+=f'<a href="{escape(li)}" target="_blank" style="color:var(--p);font-size:1.4rem;font-weight:600">LinkedIn</a>'
        if ws: socials+=f'<a href="{escape(ws)}" target="_blank" style="color:var(--p);font-size:1.4rem;font-weight:600">Website</a>'
        cards+=f'''<div style="background:#fff;border:1px solid #e0e0e0;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06)">
        <div style="width:100%;aspect-ratio:1;overflow:hidden;background:#f0f0f0">{img_html}</div>
        <div style="padding:2rem">
            <div style="font-family:var(--fh);font-size:2.2rem;font-weight:600;color:#222;margin-bottom:.4rem">{escape(name)}</div>
            <div style="font-family:var(--fb);font-size:1.3rem;font-weight:700;color:var(--p);letter-spacing:.15rem;text-transform:uppercase;margin-bottom:1.2rem">{escape(role)}</div>
            <div style="font-size:1.5rem;color:#555;line-height:1.65;margin-bottom:1.4rem">{escape(bio)}</div>
            <div style="display:flex;gap:1.4rem;flex-wrap:wrap">{socials}</div>
        </div></div>'''
    html=f'''{hd('Contributors',1)}<body class="contributors-page">{nv(1)}
<section style="padding:150px 40px 40px;text-align:center;background:#fff;min-height:60vh">
<div style="font-family:var(--fb);font-weight:700;font-size:1.4rem;letter-spacing:.4rem;text-transform:uppercase;color:var(--p);margin-bottom:1.6rem">The Team</div>
<h1 style="font-family:var(--fh);font-size:4.5rem;font-weight:600;color:#333;margin-bottom:1.6rem">Contributors</h1>
<p style="font-size:2rem;color:#666;max-width:700px;margin:0 auto">The researchers, developers, and threat intelligence analysts who build and maintain the Threat Actors encyclopedia.</p>
</section>
<section style="max-width:1200px;margin:0 auto;padding:0 40px 6rem;background:#ffffff">
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:2rem">{cards}</div>
<div style="margin-top:4rem"><h2 style="font-family:var(--fh);font-size:2.4rem;font-weight:600;color:#333;margin-bottom:2rem;text-align:center">Supporters</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1.6rem;margin-bottom:3rem">{spon_cards}</div></div>
<div style="margin-top:2rem;text-align:center;padding:3rem;background:#f5f5f5;border:1px solid #e0e0e0;border-radius:var(--r)">
<div style="font-family:var(--fh);font-size:2.4rem;font-weight:600;color:#333;margin-bottom:1.2rem">Want to Contribute?</div>
<div style="font-size:1.6rem;color:#666;max-width:600px;margin:0 auto 2rem;line-height:1.65">Add threat actor profiles, fix data, improve detection engineering, or submit custom artwork.</div>
<a href="https://github.com/adversaryvillage" target="_blank" style="display:inline-block;padding:1.4rem 3.2rem;background:var(--p);color:#fff;border-radius:var(--r);font-weight:700;font-size:1.4rem;letter-spacing:.15rem;text-transform:uppercase;text-decoration:none">Contribute on GitHub</a>
</div></section>{ft()}<script src="../js/main.js"></script></body></html>'''
    with open(os.path.join(cdir,'index.html'),'w') as f: f.write(fmt_html(html))
    print("  ✓ contributors/index.html")

if __name__=='__main__': main()