"""Deck renderer: splices the KIBS gold-standard deck (CSS, chrome, nav/break JS) and emits new slides.
Every slide builder returns (html, note) so presenter notes come from the same source."""
import re, html as H

import os
_HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.environ.get("WB_EXAMPLES") or (os.path.join(_HERE, "templates") + "/" if os.path.isdir(os.path.join(_HERE, "templates")) else
     "/root/.claude/skills/synced/46c4e867-24f6-4e25-8db5-adecbebe4172_c097c4a3-d3ad-45b5-8472-60354fdb96eb/workshop-builder/references/examples/")
SRC = open(EX + "deck.html", encoding="utf-8").read()

# ---------- template pieces ----------
_head_end = SRC.index("</head>")
HEAD = SRC[:_head_end]
HEAD = re.sub(r"<title>.*?</title>", "<title>__TITLE__</title>", HEAD, count=1, flags=re.S)
_body = SRC.index("<body>")
_first_slide = SRC.index('<!-- 1 · COVER -->')
_after_slides = SRC.index('<div class="nav-dots" id="nav-dots"></div>')
_js1 = SRC.index("<script>", _after_slides)
CHROME_POST = SRC[_after_slides:_js1]
CHROME_POST = re.sub(r'<div class="brandmark" id="brandmark">.*?</div>', '<div class="brandmark" id="brandmark"><span class="bx" style="font-family:var(--mono);letter-spacing:.14em;text-transform:uppercase;font-size:10px">CODED · KAMCO Invest</span></div>', CHROME_POST, flags=re.S)
_js1_end = SRC.index("</script>", _js1) + len("</script>")
JS_MAIN = SRC[_js1:_js1_end]
_js2 = SRC.index("<script>", _js1_end)
JS_BREAK = SRC[_js2:SRC.index("</body>")]

# strip the KIBS Day-2 demo code + its wiring/init, keep the generic engine
_a = JS_MAIN.index("/* ===== Day-2 demo JS")
_b = JS_MAIN.index("/* ===== reset per slide ===== */")
_c = JS_MAIN.index("/* ===== Phase A")
JS_MAIN = JS_MAIN[:_a] + "/*__DEMOJS__*/\n" + JS_MAIN[_c:]
# slide-title labels for the nav dots
JS_MAIN = JS_MAIN.replace("else if(id==='outcomes')L='Outcomes';",
    "else if(id==='outcomes')L='Outcomes';else if(id==='flow')L='The workflow';else if(id==='map')L='MAP test';"
    "else if(id==='hands')L='Hands-on';else if(id==='project')L='Project';else if(id==='mapend')L='MAP test';"
    "else if(id==='cert')L='Certificates';else if(m=id.match(/^t(\\d+)take$/))L='T'+m[1]+' · take-away';")
JS_MAIN = JS_MAIN.replace("e.target.closest('button,input,a,", "e.target.closest('button,input,a,.pcard,.hot,.logrow,.bars,.ctft,.wv,.poll,.flip-card,.chatwin,.mail,")
assert "/*__DEMOJS__*/" in JS_MAIN

EXTRA_CSS = r"""<style>/* ===== KAMCO Copilot components (tokens only) ===== */
.pcards{display:grid;gap:12px;max-width:1080px;width:100%;margin-top:16px}
.pcard{position:relative;background:var(--panel);border:1px solid var(--w1);border-left:3px solid var(--crimson);border-radius:12px;padding:14px 92px 14px 18px}
.pcard .pw{font-family:var(--mono);font-size:10px;letter-spacing:.16em;text-transform:uppercase;color:var(--rose-lt);font-weight:700;margin-bottom:6px;display:flex;gap:10px;align-items:center}
.pcard .pw .pn{color:var(--w5)}
.pcard .pt{font-family:var(--mono);font-size:clamp(13px,1.15vw,16px);color:var(--w9,#fff);line-height:1.55;white-space:pre-wrap}
.pcard .cp{position:absolute;top:12px;right:12px;background:var(--w06);border:1px solid var(--w1);color:var(--w7);border-radius:8px;padding:6px 10px;font:700 10px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;cursor:pointer}
.pcard .cp:hover{border-color:var(--rose);color:#fff}
.pcard .cp.ok{border-color:var(--rose);color:var(--rose-lt)}
.pcard .pl{margin-top:8px;font-size:13.5px;color:var(--w6);line-height:1.45}
.pcard .pl b{color:var(--rose-lt)}
.poll .topt.picked{border-color:var(--crimson);background:rgba(200,50,74,.16)}
.wv{display:flex;gap:8px;margin:14px 0 0}
.wv button{background:var(--w06);border:1px solid var(--w1);color:var(--w7);border-radius:30px;padding:8px 16px;font:700 12px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;cursor:pointer}
.wv button.on{background:rgba(200,50,74,.16);border-color:var(--crimson);color:#fff}
.wv-pane{display:none}.wv-pane.on{display:flex;flex-direction:column;gap:11px}
.cmsg .srcchip{display:inline-block;margin-top:8px;font-family:var(--mono);font-size:10px;letter-spacing:.06em;color:var(--rose-lt);background:rgba(200,50,74,.12);border:1px solid rgba(200,50,74,.3);border-radius:6px;padding:3px 8px}
.ctft{max-width:1060px;width:100%;margin-top:16px}
.ctft-chips{display:flex;gap:10px;flex-wrap:wrap}
.ctft-chip{background:var(--w06);border:1.5px solid var(--w1);color:var(--w7);border-radius:11px;padding:11px 16px;cursor:pointer;font:800 15px/1 var(--mf);display:flex;gap:9px;align-items:center}
.ctft-chip .k{font-family:var(--mono);font-size:11px;color:var(--w5)}
.ctft-chip.on{border-color:var(--crimson);background:rgba(200,50,74,.16);color:#fff}.ctft-chip.on .k{color:var(--rose)}
.ctft-box{margin-top:14px;background:var(--panel);border:1px solid var(--w1);border-radius:12px;padding:16px 18px;font-family:var(--mono);font-size:clamp(13px,1.15vw,16px);line-height:1.6;color:var(--w8);min-height:96px}
.ctft-box .seg{display:block}.ctft-box .seg .lab{color:var(--rose);font-weight:700;margin-right:8px}
.ctft-box .ph{color:var(--w4)}
.ctft-meter{margin-top:12px;height:8px;border-radius:6px;background:var(--w06);overflow:hidden}
.ctft-meter .f{height:100%;width:0;background:linear-gradient(90deg,var(--maroon),var(--crimson),var(--rose));transition:width .35s}
.ctft-out{margin-top:10px;font-size:15px;color:var(--w7);min-height:22px}.ctft-out b{color:#fff}
.bars{max-width:1000px;width:100%;margin-top:16px;display:flex;flex-direction:column;gap:12px}
.bar-row{display:grid;grid-template-columns:150px 1fr 90px;gap:14px;align-items:center}
.bar-row .bn{font-weight:800;font-size:15.5px}
.bar-track{position:relative;height:26px;background:var(--w06);border-radius:7px;overflow:hidden}
.bar-band{position:absolute;top:0;bottom:0;background:rgba(255,255,255,.07);border-left:1px dashed var(--w3);border-right:1px dashed var(--w3)}
.bar-fill{position:absolute;left:0;top:5px;bottom:5px;border-radius:4px;background:linear-gradient(90deg,var(--maroon),var(--mid));transition:width .6s,background .3s}
.bar-row .bv{font-family:var(--mono);font-weight:700;font-size:15px;color:var(--w8);text-align:right}
.bars.checked .bar-row.over .bar-fill{background:linear-gradient(90deg,var(--crimson),var(--rose))}
.bars.checked .bar-row.over .bv{color:var(--rose)}
.bars.checked .bar-row.over .bn::after{content:' · breach';font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--rose)}
.bar-legend{font-family:var(--mono);font-size:10.5px;color:var(--w5);letter-spacing:.06em}
.foundct{font-family:var(--mono);font-size:12px;color:var(--w6);margin-top:12px}.foundct b{color:var(--rose)}
.logtable td.num{text-align:right}
.logrow.flagged td .why{display:block;font-family:var(--mf);font-size:12px;color:var(--rose-lt);margin-top:4px}
.logrow td .why{display:none}
.mail-body .hot{white-space:normal}
.mail-body.scroll{max-height:46vh;overflow:auto}
.mail-sep{border-top:1px dashed var(--w1);margin:14px 0;font-family:var(--mono);font-size:10px;color:var(--w4);padding-top:10px;letter-spacing:.06em}
.steps-ol{counter-reset:s;list-style:none;display:grid;gap:10px;margin-top:16px;max-width:1000px}
.steps-ol li{counter-increment:s;display:flex;gap:14px;align-items:flex-start;background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.012));border:1px solid var(--w1);border-radius:12px;padding:13px 16px;font-size:clamp(15px,1.3vw,18.5px);color:var(--w8);line-height:1.45}
.steps-ol li::before{content:counter(s);flex:none;width:28px;height:28px;border-radius:50%;background:rgba(200,50,74,.16);border:1px solid var(--rose);color:var(--rose-lt);font:700 13px/26px var(--mono);text-align:center}
.steps-ol li b{color:#fff}
.timebox{display:inline-flex;align-items:center;gap:10px;margin-top:18px;font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--rose-lt);background:rgba(200,50,74,.1);border:1px solid rgba(200,50,74,.3);border-radius:30px;padding:8px 16px;font-weight:700}
.rub{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:16px;max-width:1060px}
.rub>div{background:rgba(0,0,0,.28);border:1px solid var(--w1);border-radius:10px;padding:12px}
.rub .w{font-family:var(--mono);font-size:22px;font-weight:700;color:var(--rose)}
.rub .n{font-size:13px;font-weight:700;margin-top:4px}
/* pills hug their text (gold-standard pills stretched in flex columns) */
.slide-pad>.topic-tab,.slide-pad>.term-tab,.slide-pad>.bridge-tag,.slide-pad>.badge,.slide-pad>.timebox{align-self:flex-start}
.slide-pad.center>.topic-tab,.slide-pad.center>.badge{align-self:center}
@media(max-width:900px){.bar-row{grid-template-columns:100px 1fr 70px}.rub{grid-template-columns:1fr 1fr}.pcard{padding-right:18px}.pcard .cp{position:static;margin-top:8px}}
</style>"""

DEMO_JS = r"""
/* ===== KAMCO Copilot demo components ===== */
function copyTxt(t){try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t);return;}}catch(e){}try{var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();document.execCommand('copy');document.body.removeChild(ta);}catch(e){}}
document.addEventListener('click',function(e){
  var cp=e.target.closest('.pcard .cp');if(cp){e.stopPropagation();var t=cp.parentNode.querySelector('.pt').innerText;copyTxt(t);cp.textContent='Copied';cp.classList.add('ok');setTimeout(function(){cp.textContent='Copy';cp.classList.remove('ok');},1300);return;}
  var po=e.target.closest('.poll .topt');if(po){e.stopPropagation();var box=po.closest('.poll');box.querySelectorAll('.topt').forEach(function(x){x.classList.remove('picked');});po.classList.add('picked');var n=box.querySelector('.mini-note');if(n)n.innerHTML=po.dataset.fb||'';return;}
  var hot=e.target.closest('.hot');if(hot){e.stopPropagation();var root=hot.closest('.slide');if(hot.dataset.k==='1'){hot.classList.add('found');}else{hot.classList.add('dud');}
    var f=root.querySelectorAll('.hot.found').length,tot=root.querySelectorAll('.hot[data-k="1"]').length,c=root.querySelector('.foundct b');if(c)c.textContent=f;
    var nt=root.querySelector('.hotnote');if(nt&&hot.dataset.why){nt.innerHTML=(hot.dataset.k==='1'?'<b>Found · </b>':'<b>Not this one · </b>')+hot.dataset.why;}
    if(f===tot){var w=root.querySelector('.hotwin');if(w)w.style.display='block';}return;}
  var lr=e.target.closest('.logrow');if(lr&&!lr.classList.contains('head')){e.stopPropagation();var r2=lr.closest('.slide');if(lr.dataset.bad==='1')lr.classList.add('flagged');else lr.classList.add('normal');
    var f2=r2.querySelectorAll('.logrow.flagged').length,c2=r2.querySelector('.foundct b');if(c2)c2.textContent=f2;
    if(f2===r2.querySelectorAll('.logrow[data-bad="1"]').length){var w2=r2.querySelector('.hotwin');if(w2)w2.style.display='block';}return;}
  var wv=e.target.closest('.wv button');if(wv){e.stopPropagation();var cw=wv.closest('.chatwin');cw.querySelectorAll('.wv button').forEach(function(b){b.classList.toggle('on',b===wv);});cw.querySelectorAll('.wv-pane').forEach(function(p){p.classList.toggle('on',p.dataset.p===wv.dataset.p);});return;}
  var ch=e.target.closest('.ctft-chip');if(ch){e.stopPropagation();ch.classList.toggle('on');ctftDraw(ch.closest('.ctft'));return;}
  var bc=e.target.closest('.bars-check');if(bc){e.stopPropagation();var bs=bc.closest('.slide').querySelector('.bars');bs.classList.add('checked');var n3=bc.closest('.slide').querySelector('.bars-note');if(n3)n3.style.display='block';return;}
  var fc=e.target.closest('.flip-card');if(fc){e.stopPropagation();fc.classList.toggle('flipped');return;}
  var run=e.target.closest('.chat-run');if(run){e.stopPropagation();var cw2=run.closest('.chatwin');cw2.querySelectorAll('.cmsg.hidden').forEach(function(m,i){setTimeout(function(){m.style.display='block';m.classList.remove('hidden');},350*(i+1));});run.style.display='none';return;}
});
function ctftDraw(box){var on=box.querySelectorAll('.ctft-chip.on'),segs=box.querySelectorAll('.ctft-box .seg');
  segs.forEach(function(s){var k=s.dataset.k,chip=box.querySelector('.ctft-chip[data-k="'+k+'"]');s.style.display=chip.classList.contains('on')?'block':'none';});
  var ph=box.querySelector('.ctft-box .ph');if(ph)ph.style.display=on.length?'none':'block';
  box.querySelector('.ctft-meter .f').style.width=(on.length*25)+'%';
  var outs=JSON.parse(box.dataset.out||'[]');box.querySelector('.ctft-out').innerHTML=outs[on.length]||'';}
function resetInteractives(s){
  mcReset(s);
  s.querySelectorAll('.poll .topt').forEach(function(x){x.classList.remove('picked');});s.querySelectorAll('.poll .mini-note').forEach(function(n){n.innerHTML='';});
  s.querySelectorAll('.hot').forEach(function(x){x.classList.remove('found','dud');});
  s.querySelectorAll('.logrow').forEach(function(x){x.classList.remove('flagged','normal');});
  s.querySelectorAll('.foundct b').forEach(function(x){x.textContent='0';});
  s.querySelectorAll('.hotwin,.bars-note').forEach(function(x){x.style.display='none';});
  s.querySelectorAll('.hotnote').forEach(function(x){x.innerHTML=x.dataset.def||'';});
  s.querySelectorAll('.bars').forEach(function(x){x.classList.remove('checked');});
  s.querySelectorAll('.flip-card').forEach(function(x){x.classList.remove('flipped');});
  s.querySelectorAll('.ctft').forEach(function(b){b.querySelectorAll('.ctft-chip').forEach(function(c){c.classList.remove('on');});ctftDraw(b);});
  s.querySelectorAll('.chatwin').forEach(function(cw){cw.querySelectorAll('.cmsg[data-hide="1"]').forEach(function(m){m.classList.add('hidden');m.style.display='none';});var r=cw.querySelector('.chat-run');if(r)r.style.display='';
    var first=cw.querySelector('.wv button');if(first){cw.querySelectorAll('.wv button').forEach(function(b,i){b.classList.toggle('on',i===0);});cw.querySelectorAll('.wv-pane').forEach(function(p,i){p.classList.toggle('on',i===0);});}});
}
"""

# ---------- helpers ----------
BG = '<div class="bg-grid"></div><div class="blob b1"></div>'
BG2 = '<div class="bg-grid"></div><div class="blob b1"></div><div class="blob b2"></div>'
BG3 = '<div class="bg-grid"></div><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>'
ICN_CHAT = '<svg class="icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M8 10h8M8 14h5"></path><path d="M4 5h16v12H9l-4 4z"></path></svg>'
ICN_SPARK = '<svg class="icn" viewBox="0 0 24 24"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z"></path></svg>'


def strip(s):
    return re.sub(r"<[^>]+>", "", s).replace("&amp;", "&").replace("&nbsp;", " ")


def note(t, k, h, b, say=None):
    d = dict(t=t, k=k, h=h, b=b)
    if say:
        d["say"] = say
    return d


def cover(day_label, t1, t2, sub, meta_date, meta_place, pill="CODED × KAMCO Invest · Kuwait", say=None):
    h = f'''<div class="slide active" id="cover" data-auto="0">
  <div class="cv2-bg"><div class="cv2-r1"></div><div class="cv2-r2"></div><div class="cv2-r3"></div><div class="cv2-b1"></div><div class="cv2-wash"></div></div>
  <div class="bg-grid"></div><div class="cv2-vig"></div>
  <div class="cv2">
    <div class="cv2-pill"><span class="dot"></span> {pill}</div>
    <h1 class="cv2-title"><span class="cv2-t1">{t1}</span><br><span class="cv2-t2">{t2}</span></h1>
    <p class="cv2-sub">{sub}</p>
    <div class="cv2-meta">
      <div class="cv2-mi"><svg viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="16" rx="2"></rect><path d="M3 9h18M8 3v4M16 3v4"></path></svg> {meta_date}</div>
      <div class="cv2-mi"><svg viewBox="0 0 24 24"><path d="M12 21s-7-5.5-7-11a7 7 0 0114 0c0 5.5-7 11-7 11z"></path><circle cx="12" cy="10" r="2.5"></circle></svg> {meta_place}</div>
    </div>
    <div class="cv2-standby"><span class="pdot"></span> We’ll begin shortly</div>
  </div>
  <div class="cv2-cue">Press → to begin</div>
</div>'''
    return h, note("open", "open", "Cover — " + day_label, [strip(sub)], say)


def standby(sid, eyebrow, title_html, lead, steps, time_label=None, say=None, extra="", t="open", k="open"):
    st = "".join(f"<li><span>{x}</span></li>" for x in steps)
    tb = f'<div class="timebox b in"><svg class="icn" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"></circle><path d="M12 9v4l2.5 2M9 2h6"></path></svg> {time_label}</div>' if time_label else ""
    h = f'''<div class="slide" id="{sid}" data-auto="2">{BG2}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="topic-title b in">{title_html}</h2>
  <p class="lead b in">{lead}</p>
  <ol class="steps-ol b in">{st}</ol>{extra}
  {tb}
</div></div>'''
    return h, note(t, k, strip(title_html), [strip(lead)] + [strip(x) for x in steps], say)


def hook(sid, eyebrow, q_html, inner, foot, say=None, bullets=None):
    h = f'''<div class="slide" id="{sid}" data-auto="0"><div class="bg-grid"></div>
  <div class="ph-stage"><div class="ph-glow"></div>
    <div class="ph-eyebrow">{eyebrow}</div>
    <div class="ph-q">{q_html}</div>
    {inner}
    <div style="position:relative;margin-top:18px;color:var(--w6);font-size:15px;max-width:680px">{foot}</div>
  </div></div>'''
    return h, note("open", "demo", "Hook — " + strip(q_html), bullets or [strip(foot)], say)


def outcomes(day_n, items, say=None):
    li = "".join(f'<div class="oc-item b in"><div class="oc-check"><svg viewBox="0 0 24 24"><path d="M5 12l5 5L20 7"></path></svg></div><div class="oc-txt">{x}</div></div>' for x in items)
    h = f'''<div class="slide" id="outcomes" data-auto="6">{BG2}<div class="slide-pad">
<div class="topic-eyebrow b in">What you will be able to do</div>
<h2 class="demo-h b in">By the end of Day {day_n}, <span class="hl">you will be able to:</span></h2>
<div class="oc-list">{li}</div>
</div></div>'''
    return h, note("open", "open", "Outcomes", [strip(x) for x in items], say)


def road(eyebrow, title_html, lead, items, say=None):
    it = "".join(f'<div class="ritem b in"><div class="rn">{i+1}</div><div><div class="rt">{t}</div><div class="rd">{d}</div></div></div>' for i, (t, d) in enumerate(items))
    h = f'''<div class="slide" id="road" data-auto="0">{BG2}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h b in">{title_html}</h2>
  <p class="lead b in">{lead}</p>
  <div class="road">{it}</div>
</div></div>'''
    return h, note("open", "story", "Road — " + strip(title_html), [strip(lead)] + ["<b>%d</b> %s" % (i + 1, strip(t)) for i, (t, d) in enumerate(items)], say)


def flow(sid, eyebrow, title_html, lead, steps, label, say=None, t="open"):
    fs = "".join(f'<div class="fstep"><div class="fn">{n}</div><div class="fh">{a}</div><div class="fd">{b}</div></div>' for n, a, b in steps)
    h = f'''<div class="slide" id="{sid}" data-auto="3">{BG2}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h b in">{title_html}</h2>
  <p class="lead b in">{lead}</p>
  <div class="flow b in"><div class="fl">{label}</div><div class="flow-steps">{fs}</div></div>
</div></div>'''
    return h, note(t, "story", strip(title_html), [strip(lead)] + ["%s — %s" % (strip(a), strip(b)) for n, a, b in steps], say)


def story(n, topic_label, al, text, head_html, say=None):
    h = f'''<div class="slide" id="t{n}story" data-auto="2" data-act="0{n}">{BG2}<div class="slide-pad">
  <div class="topic-tab b in">Topic {n} · {topic_label}</div><div class="bridge-tag story b in">The story</div>
  <div class="anchor b in"><span class="al">{al}</span>{text}</div>
  <h2 class="demo-h b in">{head_html}</h2>
</div></div>'''
    return h, note("t%d" % n, "story", "Story — " + al, [strip(text), "Land it: " + strip(head_html)], say)


def analogy(n, i, tab, title, text, svg, say=None):
    viz = f'<div class="ana-viz">{svg}</div>' if svg else ""
    h = f'''<div class="slide" id="t{n}a{i}" data-auto="2">{BG}<div class="slide-pad">
  <div class="term-tab b in">{tab}</div><div class="bridge-tag story b in">The analogy</div>
  <h2 class="demo-h b in">{title}</h2>
  <div class="ana-row"><div class="ana-text"><div class="anchor b in" style="border-color:var(--w1)">{text}</div></div>{viz}</div>
</div></div>'''
    return h, note("t%d" % n, "analogy", "Analogy — " + strip(title), [strip(text)], say)


def term(n, i, title_html, dt, definition, frm, to, keyline=None, say=None):
    kl = f'<div class="keyline b in">{keyline}</div>' if keyline else ""
    h = f'''<div class="slide" id="t{n}t{i}" data-auto="4">{BG}<div class="slide-pad">
  <div class="bridge-tag tech b in">The term &amp; the link</div>
  <h2 class="demo-h b in">{title_html}</h2>
  <div class="defbox b in"><span class="dt">{dt}</span> {definition}</div>
  <div class="link-line b in"><div class="ll-from">{frm}</div><div class="ll-arrow">→</div><div class="ll-to">{to}</div></div>
  {kl}
</div></div>'''
    b = ["<b>%s</b> — %s" % (dt, strip(definition)), strip(frm) + " → " + strip(to)]
    if keyline:
        b.append(strip(keyline))
    return h, note("t%d" % n, "term", "Term — " + dt.title(), b, say)


def check(n, i, q, opts, say=None):
    ob = "".join(f'<button class="mc-opt" data-k="{1 if c else 0}" data-fb="{H.escape(fb, quote=True)}">{t}</button>' for t, c, fb in opts)
    h = f'''<div class="slide" id="t{n}d{i}" data-auto="2">{BG}<div class="slide-pad">
  <div class="badge disc b in">{ICN_CHAT} Mini check · your call</div>
  <div class="mini b in"><div class="mini-q">{q}</div>
    <div class="mc-opts">{ob}</div><div class="mc-fb"></div></div>
</div></div>'''
    right = [t for t, c, fb in opts if c][0]
    return h, note("t%d" % n, "check", "Your call — " + strip(q), ["Answer: <b>%s</b>" % strip(right), [fb for t, c, fb in opts if c][0]], say), dict(q=strip(q), a=strip(right), why=[fb for t, c, fb in opts if c][0])


def demo(n, i, badge, title_html, lead, inner, say=None, bullets=None, sid=None):
    sid = sid or f"t{n}d{i}"
    h = f'''<div class="slide" id="{sid}" data-auto="2">{BG}<div class="slide-pad">
  <div class="badge scored b in"><span class="ld"></span> {badge}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <p class="lead b in">{lead}</p>
  <div class="b in" style="width:100%">{inner}</div>
</div></div>'''
    return h, note("t%d" % n if n else "open", "demo", "Live demo — " + strip(title_html), bullets or [strip(lead)], say)


def prompts(cards):
    """cards: list of (where, text, look_for)"""
    out = []
    for j, (where, txt, look) in enumerate(cards, 1):
        lk = f'<div class="pl"><b>Check:</b> {look}</div>' if look else ""
        out.append(f'<div class="pcard"><div class="pw"><span class="pn">{j:02d}</span>{where}</div><div class="pt">{H.escape(txt)}</div>{lk}<button class="cp">Copy</button></div>')
    return '<div class="pcards">' + "".join(out) + "</div>"


def case(n, head_html, big, unit, dec, name, text, stats, nxt, say=None, sid=None):
    def cu(v, u, d):
        if isinstance(v, (int, float)):
            return f'<span class="countup" data-count="{v}"' + (f' data-dec="{d}"' if d else "") + (f' data-suffix="{u}"' if u else "") + "></span>"
        return v
    st = "".join(f'<div class="st3"><div class="v">{cu(v, u, d)}</div><div class="l">{l}</div></div>' for v, u, d, l in stats)
    h = f'''<div class="slide" id="{sid or ('t%dcase' % n)}" data-auto="3">{BG3}<div class="slide-pad">
  <div class="bridge-tag tech b in">When it was real</div>
  <h2 class="demo-h sm b in">{head_html}</h2>
  <div class="case-hero b in"><div class="big">{cu(big, unit, dec)}</div><div class="ht"><span class="nm">{name}</span>{text}</div></div>
  <div class="stat3 b in">{st}</div>
  <div class="src b in"><strong>Confirm figures before quoting live.</strong> <span style="color:var(--rose-lt)">{nxt}</span></div>
</div></div>'''
    return h, note("t%d" % n, "case", "Real case — " + strip(name), [strip(text)] + ["%s%s — %s" % (v, u or "", strip(l)) for v, u, d, l in stats] + ["Confirm figures before quoting."], say)


def take(n, eyebrow, punch_html, sm=None, say=None):
    s = f'<span class="sm">{sm}</span>' if sm else ""
    h = f'''<div class="slide" id="t{n}take" data-auto="2">{BG2}<div class="slide-pad center">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <div class="close-punch b in">{punch_html}{s}</div>
</div></div>'''
    return h, note("t%d" % n, "close", "Take-away", [strip(punch_html)] + ([strip(sm)] if sm else []), say)


def pause(n, say=None):
    h = f'''<div class="slide" id="qc{n}" data-auto="3">{BG}
<div class="qc"><div class="qc-marks b in">? ? ?</div><div class="qc-title b in">Let's pause here.</div><div class="qc-sub b in">Three questions before we move on — what is unclear, or what would you push back on?</div></div>
</div>'''
    return h, note("t%d" % n, "pause", "Pause — three questions", ["Take three questions. Park long ones for the break."], say)


def close(eyebrow, title_html, lead, badge, say=None):
    h = f'''<div class="slide" id="close" data-auto="3">{BG3}
  <div class="slide-pad center" style="justify-content:center">
    <div class="topic-eyebrow b in">{eyebrow}</div>
    <h2 class="topic-title b in">{title_html}</h2>
    <p class="lead b in" style="max-width:820px">{lead}</p>
    <div class="cert-badge b in" style="margin-top:22px"><svg class="icn" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="12" cy="9" r="6"></circle><path d="M9 14l-2 7 5-3 5 3-2-7"></path></svg> {badge}</div>
  </div>
</div>'''
    return h, note("close", "close", "Wrap — " + strip(title_html), [strip(lead)], say)


def mailbox(win_title, frm, to, subj, body_html, attach=None, scroll=False):
    at = f'<div class="mrow"><span class="k">Attach</span><span class="v"><b>{attach}</b></span></div>' if attach else ""
    return f'''<div class="mail"><div class="mail-bar"><span class="d r"></span><span class="d y"></span><span class="d g"></span><span class="t">{win_title}</span></div>
<div class="mail-head"><div class="mrow"><span class="k">From</span><span class="v"><b>{frm}</b></span></div><div class="mrow"><span class="k">To</span><span class="v">{to}</span></div><div class="mrow"><span class="k">Subject</span><span class="v"><b>{subj}</b></span></div>{at}</div>
<div class="mail-body{' scroll' if scroll else ''}">{body_html}</div></div>'''


def hot(text, ok, why):
    return f'<span class="hot" data-k="{1 if ok else 0}" data-why="{H.escape(why, quote=True)}">{text}</span>'


def chat(who, sub, msgs, run_label=None, toggle=None):
    """msgs: list of (side, html, hidden). toggle: list of (key,label,[msgs])"""
    def m(side, h, hidden=False):
        hd = ' data-hide="1"' if hidden else ""
        return f'<div class="cmsg {side}{" hidden" if hidden else ""}"{hd}{" style=\"display:none\"" if hidden else ""}>{h}</div>'
    if toggle:
        btns = "".join(f'<button data-p="{k}" class="{"on" if j == 0 else ""}">{l}</button>' for j, (k, l, ms) in enumerate(toggle))
        panes = "".join(f'<div class="wv-pane{" on" if j == 0 else ""}" data-p="{k}">' + "".join(m(*x) for x in ms) + "</div>" for j, (k, l, ms) in enumerate(toggle))
        body = f'<div class="wv">{btns}</div>' + panes
    else:
        body = "".join(m(*x) for x in msgs)
    run = f'<button class="btn chat-run" style="margin-top:6px">{run_label}</button>' if run_label else ""
    return f'''<div class="chatwin"><div class="chat-bar"><div class="chat-av">{ICN_SPARK}</div><div><div class="chat-who">{who}</div><div class="chat-sub">{sub}</div></div></div>
<div class="chat-body">{body}{run}</div></div>'''


def page(title, back_href, slides_html, note_list):
    body = ('<body>\n<a class="deck-back" href="%s" title="Back to the day overview" aria-label="Back to the day overview"><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"></path></svg><span>Back</span></a>\n'
            '<div id="prail-wrap"><div id="prail"></div></div>\n<div class="brand"></div>\n' % back_href)
    js = JS_MAIN.replace("/*__DEMOJS__*/", DEMO_JS)
    return HEAD.replace("__TITLE__", H.escape(title)) + EXTRA_CSS + "</head>\n" + body + "\n".join(slides_html) + "\n" + CHROME_POST + js + "\n\n" + JS_BREAK + "</body></html>"
