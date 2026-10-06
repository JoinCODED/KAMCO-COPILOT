"""Block-structure slide types (Mastering Copilot flow): MAP timer + QR, the wall, card grids, AI circles,
autocomplete, token build, confidence gap, lab intro, break timers, bridges, CTFT parts, prompt rounds, verify."""
import json, html as H
import deckkit
from deckkit import BG, BG2, BG3, note, strip

QRLIB = open("node_modules/qrcode-generator/qrcode.js", encoding="utf-8").read()

CSS = r"""<style>/* ===== block-structure components ===== */
.slide-pad>.topic-eyebrow{align-self:flex-start}.slide-pad.center>.topic-eyebrow{align-self:center}
.map-row{display:flex;gap:56px;align-items:center;justify-content:center;flex-wrap:wrap;margin-top:18px}
.tmr{display:flex;flex-direction:column;align-items:center;gap:16px}
.tmr-clock{font-family:var(--mono);font-weight:700;font-size:clamp(84px,12vw,170px);letter-spacing:-4px;line-height:1;color:#fff;text-shadow:0 0 50px rgba(200,50,74,.35)}
.tmr-clock.done{color:var(--rose)}
.tmr-ctl{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}
.tmr-ctl button{background:var(--w06);border:1px solid var(--w1);color:#fff;border-radius:11px;padding:11px 16px;font:700 13px/1 var(--mono);cursor:pointer}
.tmr-ctl button:hover{border-color:var(--rose)}
.tmr-ctl button.main{background:var(--crimson);border-color:var(--crimson)}
.tmr-back{font-family:var(--mono);font-size:14px;color:var(--w6);letter-spacing:.08em}.tmr-back b{color:var(--rose-lt)}
.qrbox{display:flex;flex-direction:column;align-items:center;gap:12px}
.qr{width:230px;height:230px;background:#fff;border-radius:16px;padding:12px;display:flex;align-items:center;justify-content:center}
.qr svg{width:100%;height:100%}
.qr.empty{background:transparent;border:2px dashed var(--w2);color:var(--w5);font:600 13px/1.4 var(--mf);text-align:center;padding:20px}
.qr-link{font-weight:800;color:#fff;text-decoration:none;border-bottom:1px solid var(--rose);padding-bottom:2px}
.qr-set{display:flex;gap:6px}.qr-set input{width:220px;background:var(--base);border:1px solid var(--w1);color:#fff;border-radius:9px;padding:9px 11px;font:500 12px var(--mono)}
.qr-set button{background:var(--w06);border:1px solid var(--w1);color:#fff;border-radius:9px;padding:0 12px;font:700 12px var(--mono);cursor:pointer}
.qr-edit{background:none;border:none;color:var(--w4);font:600 11px var(--mono);cursor:pointer;letter-spacing:.06em}
.wall{width:100%;max-width:1120px;margin-top:18px}
.wall-in{display:flex;gap:10px}
.wall-input{flex:1;min-width:0;background:var(--panel);border:1.5px solid var(--w1);border-radius:13px;padding:16px 18px;color:#fff;font:600 clamp(16px,1.4vw,20px) var(--mf)}
.wall-input:focus{outline:none;border-color:var(--crimson)}
.wall-board{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px;min-height:120px;align-content:flex-start}
.wchip{position:relative;background:linear-gradient(160deg,var(--surf2),var(--panel));border:1px solid var(--w1);border-left:3px solid var(--crimson);border-radius:12px;padding:13px 34px 13px 16px;font-size:clamp(15px,1.3vw,19px);font-weight:700;color:#fff;animation:fadeUp .3s ease;max-width:520px}
.wchip .x{position:absolute;top:6px;right:9px;background:none;border:none;color:var(--w4);cursor:pointer;font-size:14px}
.wall.ro .wchip{padding-right:16px}.wall.ro .wchip .x{display:none}
.wall-count{font-family:var(--mono);font-size:12px;color:var(--w5);margin-top:12px}.wall-count b{color:var(--rose)}
.wall-empty{color:var(--w4);font-size:15px}
.kcards{display:grid;gap:14px;margin-top:18px;width:100%;max-width:1160px}
.kcard{background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.012));border:1px solid var(--w1);border-radius:15px;padding:20px 20px 18px}
.kcard .ki{font-size:30px;line-height:1;margin-bottom:12px}
.kcard .kt{font-size:clamp(17px,1.45vw,21px);font-weight:800;letter-spacing:-.3px;color:#fff}
.kcard .kd{font-size:clamp(13.5px,1.1vw,16px);color:var(--w7);margin-top:7px;line-height:1.45}
.kcard .kd b{color:var(--rose-lt)}
.kcard .kn{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--rose-lt);font-weight:700;margin-bottom:8px}
.kcard.neg{border-style:dashed;opacity:.85}.kcard.neg .kt{color:var(--w7)}
.notrow{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.notrow span{font-family:var(--mono);font-size:12px;letter-spacing:.06em;color:var(--w6);border:1px dashed var(--w2);border-radius:30px;padding:7px 13px}
.circles{display:flex;gap:40px;align-items:center;flex-wrap:wrap;margin-top:10px;width:100%}
.circles svg{width:min(560px,100%);height:auto;flex:none}
.circles .clist{flex:1;min-width:260px;display:flex;flex-direction:column;gap:10px}
.circles .cl{display:flex;gap:12px;align-items:baseline;font-size:clamp(14px,1.2vw,17px);color:var(--w7)}
.circles .cl b{color:#fff;min-width:140px;display:inline-block}
.ac{max-width:1000px;width:100%;margin-top:18px}
.ac-s{font-size:clamp(30px,4.2vw,58px);font-weight:800;letter-spacing:-1.2px;line-height:1.15;color:#fff;min-height:2.4em}
.ac-blank{display:inline-block;min-width:3.4em;border-bottom:4px dashed var(--rose);color:transparent}
.ac-blank.on{color:var(--rose);border-bottom-style:solid}
.tok{max-width:1060px;width:100%;margin-top:20px}
.tok-out{display:flex;flex-wrap:wrap;gap:8px;min-height:84px;align-items:flex-end}
.tk{display:inline-flex;flex-direction:column;align-items:center;gap:5px;animation:fadeUp .25s ease}
.tk .w{font-size:clamp(20px,2.2vw,32px);font-weight:800;color:#fff;background:rgba(200,50,74,.12);border:1px solid rgba(200,50,74,.3);border-radius:9px;padding:6px 11px}
.tk .p{font-family:var(--mono);font-size:11px;color:var(--w5)}
.gap2{display:grid;grid-template-columns:1fr;gap:16px;max-width:900px;width:100%;margin-top:22px}
.gap2 .gl{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--w6);margin-bottom:8px;display:flex;justify-content:space-between}
.gap2 .gt{height:30px;border-radius:8px;background:var(--w06);overflow:hidden}
.gap2 .gf{height:100%;border-radius:8px;background:linear-gradient(90deg,var(--mid),var(--crimson),var(--rose));transition:width .9s}
.gap2 .gf.q{background:repeating-linear-gradient(45deg,var(--w1),var(--w1) 10px,transparent 10px,transparent 20px);width:100%}
.labx{display:grid;gap:12px;margin-top:18px;max-width:1000px;width:100%}
.labx .lx{display:grid;grid-template-columns:84px 1fr 90px;gap:16px;align-items:center;background:linear-gradient(180deg,rgba(255,255,255,.045),rgba(255,255,255,.012));border:1px solid var(--w1);border-radius:13px;padding:15px 18px}
.labx .lc{font-family:var(--mono);font-weight:700;color:var(--rose);font-size:15px}
.labx .ln{font-weight:800;font-size:clamp(16px,1.4vw,20px);color:#fff}.labx .ld{font-size:14px;color:var(--w6);margin-top:3px}
.labx .lm{font-family:var(--mono);font-size:13px;color:var(--w7);text-align:right}
.succ{margin-top:16px;font-size:clamp(16px,1.4vw,19px);color:var(--w7)}.succ b{color:var(--rose-lt)}
.labgo{margin-top:18px;align-self:flex-start;text-decoration:none}
.bridge-l1{font-size:clamp(22px,2.6vw,34px);color:var(--w6);font-weight:600;max-width:980px;line-height:1.35}
.bridge-l2{font-size:clamp(28px,3.6vw,50px);color:#fff;font-weight:800;letter-spacing:-1.2px;max-width:1080px;line-height:1.15;margin-top:18px}
.bridge-l2 b{color:var(--rose)}
.wvs{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:18px;max-width:1100px;width:100%}
.wvs .wv-col{border-radius:14px;padding:18px 20px;border:1px solid var(--w1)}
.wvs .wv-col.in{background:rgba(200,50,74,.08);border-color:rgba(200,50,74,.35)}
.wvs .wv-col h4{font-size:18px;font-weight:800;margin-bottom:8px}.wvs .wv-col p{font-size:15px;color:var(--w7);line-height:1.5}
.ws{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px;max-width:1100px;width:100%}
.ws .wk,.ws .st{border-radius:13px;padding:16px 18px;font-family:var(--mono);font-size:clamp(13px,1.15vw,16px);line-height:1.55}
.ws .wk{background:rgba(255,255,255,.03);border:1px dashed var(--w2);color:var(--w6)}
.ws .st{background:rgba(200,50,74,.08);border:1px solid rgba(200,50,74,.34);color:#fff}
.ws .lab{display:block;font-size:10px;letter-spacing:.16em;text-transform:uppercase;margin-bottom:8px;font-weight:700}
.ws .wk .lab{color:var(--w5)}.ws .st .lab{color:var(--rose-lt)}
.chiprow{display:flex;gap:8px;flex-wrap:wrap;margin-top:14px;align-items:center}
.chiprow .cl{font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--w5);margin-right:6px}
.chiprow span.c{font-size:14px;font-weight:700;color:#fff;background:var(--w06);border:1px solid var(--w1);border-radius:30px;padding:6px 13px}
.bigletter{font-family:var(--mono);font-weight:700;font-size:clamp(70px,9vw,120px);color:var(--rose);line-height:.9;margin-right:18px}
.ctft-head{display:flex;align-items:center}
.round-p{max-width:1100px;width:100%;margin-top:16px;background:var(--panel);border:1px solid var(--w1);border-radius:14px;padding:18px 20px;font-family:var(--mono);font-size:clamp(14px,1.25vw,17px);line-height:1.65;color:var(--w6)}
.round-p .seg{display:inline}.round-p .seg.new{color:#fff;background:rgba(200,50,74,.18);border-radius:5px;padding:1px 4px}
.round-p .seg .tag{font-size:10px;letter-spacing:.12em;color:var(--rose-lt);margin-right:6px;text-transform:uppercase}
.qmeter{max-width:1100px;width:100%;margin-top:16px}
.qmeter .ql{display:flex;justify-content:space-between;font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--w6);margin-bottom:8px}.qmeter .ql b{color:var(--rose-lt)}
.qmeter .qt{height:14px;border-radius:8px;background:var(--w06);overflow:hidden}.qmeter .qf{height:100%;background:linear-gradient(90deg,var(--maroon),var(--crimson),var(--rose));border-radius:8px}
.vfy{max-width:1000px;width:100%;margin-top:18px}
.vfy .say{background:var(--panel);border:1px solid var(--w1);border-radius:14px;padding:18px 20px;font-size:clamp(18px,1.7vw,24px);color:#fff;font-weight:600}
.vfy .say mark{background:rgba(233,196,106,.25);color:#fff;border-radius:4px;padding:0 4px}
.vfy .real{display:none;margin-top:14px;background:rgba(200,50,74,.08);border:1px solid rgba(200,50,74,.34);border-radius:14px;padding:16px 20px;font-size:clamp(16px,1.5vw,21px);color:var(--w8)}.vfy .real b{color:var(--rose-lt)}
.vfy.open .real{display:block}
.drawbox{display:flex;gap:30px;align-items:center;margin-top:18px;flex-wrap:wrap}
.drawbox .shape{width:300px;height:220px;border:2px dashed var(--w2);border-radius:16px;display:flex;align-items:center;justify-content:center;color:var(--w4);font-size:60px}
.drawbox .shape svg{display:none;width:100%;height:100%}.drawbox.open .shape svg{display:block}.drawbox.open .shape .qm{display:none}
@media(max-width:900px){.wvs,.ws{grid-template-columns:1fr}.labx .lx{grid-template-columns:60px 1fr}.labx .lm{grid-column:2;text-align:left}}
</style>"""

JS = r"""
/* ===== timers (MAP + breaks) ===== */
var TMRS=[];
function tmrFmt(s){s=Math.max(0,s);return Math.floor(s/60)+':'+(s%60<10?'0':'')+(s%60);}
function tmrDraw(t){var c=t.querySelector('.tmr-clock');c.textContent=tmrFmt(t._left);c.classList.toggle('done',t._left<=0);var b=t.querySelector('[data-act="start"]');if(b)b.textContent=t._run?'Pause':'Start';}
function tmrInit(t){if(t._init)return;t._init=1;t._left=+t.dataset.sec;t._run=false;TMRS.push(t);tmrDraw(t);}
setInterval(function(){TMRS.forEach(function(t){if(t._run){t._left--;if(t._left<=0){t._left=0;t._run=false;if(typeof sfx==='function')sfx('times-up');}tmrDraw(t);}});},1000);
document.addEventListener('click',function(e){var b=e.target.closest('.tmr-ctl button');if(!b)return;e.stopPropagation();var t=b.closest('.tmr');tmrInit(t);var a=b.dataset.act,d=+(b.dataset.d||0);
  if(a==='start')t._run=!t._run;else if(a==='add')t._left+=d;else if(a==='sub')t._left=Math.max(0,t._left-d);else if(a==='reset'){t._left=+t.dataset.sec;t._run=false;}tmrDraw(t);});
/* ===== QR (MAP test link) ===== */
var QR_URLS=__QRURLS__;
function qrGet(k){try{var v=localStorage.getItem('kamco_qr_'+k);if(v)return v;}catch(e){}return QR_URLS[k]||'';}
function qrDraw(box){var k=box.dataset.k,u=qrGet(k),q=box.querySelector('.qr'),a=box.querySelector('.qr-link'),set=box.querySelector('.qr-set'),ed=box.querySelector('.qr-edit');
  if(u){try{var qr=qrcode(0,'M');qr.addData(u);qr.make();q.innerHTML=qr.createSvgTag({cellSize:4,margin:0,scalable:true});q.classList.remove('empty');}catch(err){q.textContent='Link too long for a QR code';}
    a.href=u;a.style.display='';set.style.display='none';ed.style.display='';}
  else{q.innerHTML='Paste the MAP test link below — the QR code appears here.';q.classList.add('empty');a.style.display='none';set.style.display='';ed.style.display='none';}}
document.addEventListener('click',function(e){var s=e.target.closest('.qr-set button');if(s){e.stopPropagation();var box=s.closest('.qrbox'),v=box.querySelector('.qr-set input').value.trim();if(!v)return;try{localStorage.setItem('kamco_qr_'+box.dataset.k,v);}catch(er){QR_URLS[box.dataset.k]=v;}qrDraw(box);return;}
  var ed=e.target.closest('.qr-edit');if(ed){e.stopPropagation();var bx=ed.closest('.qrbox');bx.querySelector('.qr-set').style.display='';bx.querySelector('.qr-set input').value=qrGet(bx.dataset.k);}});
document.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.closest&&e.target.closest('.qr-set')){var b=e.target.closest('.qr-set').querySelector('button');b.click();}});
/* ===== the wall ===== */
var WALL={};
function wallLoad(k){if(WALL[k])return WALL[k];var v=[];try{v=JSON.parse(localStorage.getItem('kamco_wall_'+k)||'[]');}catch(e){}WALL[k]=v;return v;}
function wallSave(k){try{localStorage.setItem('kamco_wall_'+k,JSON.stringify(WALL[k]));}catch(e){}}
function wallDraw(){document.querySelectorAll('.wall').forEach(function(w){var k=w.dataset.k,v=wallLoad(k),bd=w.querySelector('.wall-board');bd.innerHTML='';
  if(!v.length&&w.classList.contains('ro'))bd.innerHTML='<div class="wall-empty">The wall is empty — add answers on the ice-breaker slide.</div>';
  v.forEach(function(t,i){var c=document.createElement('div');c.className='wchip';c.textContent=t;var x=document.createElement('button');x.className='x';x.textContent='×';x.dataset.i=i;c.appendChild(x);bd.appendChild(c);});
  var ct=w.querySelector('.wall-count b');if(ct)ct.textContent=v.length;});}
function wallAdd(w){var inp=w.querySelector('.wall-input'),t=inp.value.trim();if(!t)return;wallLoad(w.dataset.k).push(t);wallSave(w.dataset.k);inp.value='';wallDraw();inp.focus();}
document.addEventListener('click',function(e){var a=e.target.closest('.wall-add');if(a){e.stopPropagation();wallAdd(a.closest('.wall'));return;}
  var x=e.target.closest('.wchip .x');if(x){e.stopPropagation();var w=x.closest('.wall');wallLoad(w.dataset.k).splice(+x.dataset.i,1);wallSave(w.dataset.k);wallDraw();}});
document.addEventListener('keydown',function(e){if(e.key==='Enter'&&e.target.classList&&e.target.classList.contains('wall-input')){e.preventDefault();wallAdd(e.target.closest('.wall'));}});
/* ===== human autocomplete ===== */
document.addEventListener('click',function(e){var b=e.target.closest('.ac-btn');if(!b)return;e.stopPropagation();var ac=b.closest('.ac'),items=JSON.parse(ac.dataset.items),i=+(ac.dataset.i||0),bl=ac.querySelector('.ac-blank');
  if(!bl.classList.contains('on')){bl.textContent=items[i][1];bl.classList.add('on');b.textContent=i<items.length-1?'Next sentence →':'Start again';}
  else{i=(i+1)%items.length;ac.dataset.i=i;acDraw(ac);b.textContent='Reveal the next word';}});
function acDraw(ac){var items=JSON.parse(ac.dataset.items),i=+(ac.dataset.i||0);ac.querySelector('.ac-s').innerHTML=items[i][0]+' <span class="ac-blank">'+items[i][1]+'</span>';}
/* ===== token build ===== */
document.addEventListener('click',function(e){var b=e.target.closest('.tok-btn');if(!b)return;e.stopPropagation();var tk=b.closest('.tok'),out=tk.querySelector('.tok-out'),items=JSON.parse(tk.dataset.items);out.innerHTML='';b.disabled=true;
  items.forEach(function(it,i){setTimeout(function(){var d=document.createElement('span');d.className='tk';d.innerHTML='<span class="w">'+it[0]+'</span><span class="p">'+it[1]+'</span>';out.appendChild(d);if(i===items.length-1)b.disabled=false;},420*i);});});
/* ===== reveals ===== */
document.addEventListener('click',function(e){var b=e.target.closest('.reveal-btn');if(!b)return;e.stopPropagation();var t=b.closest('[data-reveal]');t.classList.add('open');b.style.display='none';});
"""

JS_RESET = r"""
  s.querySelectorAll('.tmr').forEach(function(t){tmrInit(t);if(s.id.indexOf('break')===0&&!t._run&&t._left===+t.dataset.sec){t._run=true;}tmrDraw(t);});
  s.querySelectorAll('.qrbox').forEach(qrDraw);
  wallDraw();
  s.querySelectorAll('.ac').forEach(function(ac){ac.dataset.i=0;acDraw(ac);var b=ac.querySelector('.ac-btn');if(b)b.textContent='Reveal the next word';});
  s.querySelectorAll('.tok .tok-out').forEach(function(o){o.innerHTML='';});
  s.querySelectorAll('[data-reveal]').forEach(function(r){r.classList.remove('open');var b=r.querySelector('.reveal-btn');if(b)b.style.display='';});
"""


def install(qr_urls):
    """Patch deckkit so pages built after this include the block components."""
    if getattr(deckkit, "_k2", False):
        return
    deckkit._k2 = True
    deckkit.EXTRA_CSS = deckkit.EXTRA_CSS + CSS
    js = JS.replace("__QRURLS__", json.dumps(qr_urls))
    deckkit.DEMO_JS = deckkit.DEMO_JS.replace("function resetInteractives(s){\n  mcReset(s);", "function resetInteractives(s){\n  mcReset(s);" + JS_RESET) + js
    deckkit.JS_MAIN = deckkit.JS_MAIN.replace("e.target.closest('button,input,a,", "e.target.closest('button,input,a,.wall,.qrbox,.tmr,.ac,.tok,.vfy,.drawbox,")
    deckkit.JS_MAIN = deckkit.JS_MAIN.replace("else if(m=id.match(/^break(\\d+)$/))L='Break '+m[1];",
        "else if(m=id.match(/^break(\\d+)$/))L='Break '+m[1];else if(id==='ice')L='Ice breaker';else if(id==='recap')L='Recap';else if(id==='setup')L='Setup check';else if(id==='rules')L='Ground rules';else if(m=id.match(/^b(\\d+)\\w*$/))L='Block '+m[1];")
    # QR library before the main script
    deckkit.QR_PREFIX = "<script>/* qrcode-generator (MIT, Kazuhiko Arase) */\n" + QRLIB + "\n</script>\n"


def page(title, back, slides):
    html = deckkit.page(title, back, slides, [])
    i = html.index("<script>\nvar slides=") if "<script>\nvar slides=" in html else html.index("<script>")
    return html[:i] + deckkit.QR_PREFIX + html[i:]


# ---------------- slide builders ----------------
def map_slide(sid, eyebrow, title_html, minutes, k, t="open", say=None):
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG2}<div class="slide-pad center" style="justify-content:center;align-items:center;text-align:center">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="topic-title b in">{title_html}</h2>
  <div class="map-row b in">
    <div class="tmr" data-sec="{minutes*60}"><div class="tmr-clock">{minutes}:00</div><div class="tmr-ctl"><button class="main" data-act="start">Start</button><button data-act="add" data-d="120">+2 min</button><button data-act="reset">Reset</button></div></div>
    <div class="qrbox" data-k="{k}"><div class="qr empty"></div><a class="qr-link" target="_blank" rel="noopener">Open the MAP test ↗</a><div class="qr-set"><input placeholder="Paste the MAP test link"><button>Set</button></div><button class="qr-edit">change link</button></div>
  </div>
</div></div>'''
    return h, note(t, "open", strip(title_html), ["Start the 30-minute timer. Trainees scan the QR code or open the link.", "If the QR is empty: paste the MAP link under it once — the deck remembers it on this laptop."], say)


def wall_slide(sid, eyebrow, title_html, sub, placeholder, k, t="open", say=None):
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG2}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h b in">{title_html}</h2>
  <p class="lead b in">{sub}</p>
  <div class="wall b in" data-k="{k}"><div class="wall-in"><input class="wall-input" placeholder="{H.escape(placeholder)}"><button class="btn wall-add">Pin it</button></div><div class="wall-board"></div><div class="wall-count"><b>0</b> pinned</div></div>
</div></div>'''
    return h, note(t, "demo", strip(title_html), [strip(sub), "Type each answer the room calls out, press Enter. Click × to remove one."], say)


def recap_slide(sid, eyebrow, title_html, k, actions, say=None):
    ac = "".join(f"<li><span>{a}</span></li>" for a in actions)
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG2}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h b in">{title_html}</h2>
  <div class="wall ro b in" data-k="{k}"><div class="wall-board"></div></div>
  <ol class="steps-ol b in">{ac}</ol>
</div></div>'''
    return h, note("close", "close", strip(title_html), [strip(a) for a in actions], say)


def cards_slide(sid, t, kind, eyebrow, title_html, sub, cards, bottom=None, cols=None, nots=None, say=None, bullets=None):
    cols = cols or min(len(cards), 4)
    cs = "".join(f'<div class="kcard{" neg" if c.get("neg") else ""}">' + (f'<div class="kn">{c["n"]}</div>' if c.get("n") else "") + (f'<div class="ki">{c["i"]}</div>' if c.get("i") else "")
                 + f'<div class="kt">{c["t"]}</div>' + (f'<div class="kd">{c["d"]}</div>' if c.get("d") else "") + "</div>" for c in cards)
    nt = '<div class="notrow b in">' + "".join(f"<span>{x}</span>" for x in nots) + "</div>" if nots else ""
    bt = f'<div class="keyline b in">{bottom}</div>' if bottom else ""
    sb = f'<p class="lead b in">{sub}</p>' if sub else ""
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>{sb}
  <div class="kcards b in" style="grid-template-columns:repeat({cols},1fr)">{cs}</div>{nt}{bt}
</div></div>'''
    return h, note(t, kind, strip(title_html), bullets or ([strip(sub)] if sub else []) + ["<b>%s</b> — %s" % (strip(c["t"]), strip(c.get("d", ""))) for c in cards] + ([strip(bottom)] if bottom else []), say)


def circles_slide(sid, t, eyebrow, title_html, layers, bottom, say=None):
    # layers: outer -> inner (label, example)
    n = len(layers); cx, cy = 280, 210; svg = ""
    for i, (lab, ex) in enumerate(layers):
        rx = 270 - i * 50; ry = 200 - i * 37; y = cy + (i * 20)
        hl = i == n - 1
        svg += (f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="{ry}" fill="{"rgba(200,50,74,.22)" if hl else "rgba(255,255,255,%.3f)" % (0.02 + i * 0.012)}" stroke="{"var(--rose)" if hl else "var(--w3)"}" stroke-width="{2.5 if hl else 1.5}"></ellipse>'
                f'<text x="{cx}" y="{(y + 6) if hl else (y - ry + 26)}" text-anchor="middle" style="font:800 {17 if hl else 15}px var(--mf);fill:{"#fff" if hl else "var(--w8)"}">{lab}</text>')
    lst = "".join(f'<div class="cl"><b>{lab}</b><span>{ex}</span></div>' for lab, ex in layers)
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <div class="circles b in"><svg viewBox="0 0 560 430">{svg}</svg><div class="clist">{lst}</div></div>
  <div class="keyline b in">{bottom}</div>
</div></div>'''
    return h, note(t, "term", strip(title_html), ["<b>%s</b> — %s" % (a, strip(b)) for a, b in layers] + [strip(bottom)], say)


def ac_slide(sid, t, eyebrow, title_html, items, bottom, say=None):
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG2}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <div class="ac b in" data-items='{H.escape(json.dumps(items), quote=True)}'><div class="ac-s"></div><div class="demo-controls"><button class="btn ac-btn">Reveal the next word</button></div></div>
  <div class="keyline b in">{bottom}</div>
</div></div>'''
    return h, note(t, "demo", strip(title_html), ["Read the sentence; the room shouts the next word; then reveal."] + ["%s … <b>%s</b>" % (a, b) for a, b in items] + [strip(bottom)], say)


def tok_slide(sid, t, eyebrow, title_html, lead, items, bottom, say=None):
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <p class="lead b in">{lead}</p>
  <div class="tok b in" data-items='{H.escape(json.dumps(items), quote=True)}'><div class="tok-out"></div><div class="demo-controls"><button class="btn tok-btn">▸ Watch it build an answer</button></div></div>
  <div class="keyline b in">{bottom}</div>
</div></div>'''
    return h, note(t, "demo", strip(title_html), [strip(lead), "Click to build the answer one token at a time. The number is how likely each piece was.", strip(bottom)], say)


def gap_slide(sid, t, eyebrow, title_html, lead, example, bottom, say=None):
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <p class="lead b in">{lead}</p>
  <div class="vfy b in" data-reveal><div class="say">{example}</div>
   <div class="gap2"><div><div class="gl"><span>How sure it sounds</span><span>100%</span></div><div class="gt"><div class="gf" style="width:100%"></div></div></div>
   <div><div class="gl"><span>How correct it is</span><span>??%</span></div><div class="gt"><div class="gf q"></div></div></div></div></div>
  <div class="keyline b in">{bottom}</div>
</div></div>'''
    return h, note(t, "term", strip(title_html), [strip(lead), strip(example), strip(bottom)], say)


def lab_intro(sid, t, eyebrow, title_html, rows, success, href, say=None, extra=None):
    rs = "".join(f'<div class="lx"><div class="lc">{c}</div><div><div class="ln">{n}</div><div class="ld">{d}</div></div><div class="lm">{m}</div></div>' for c, n, d, m in rows)
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG2}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <div class="labx b in">{rs}</div>
  <div class="succ b in">✓ {success}</div>{('<div class="succ b in">⚡ <b>Finished early?</b> ' + extra + '</div>') if extra else ''}
  <a class="btn labgo b in" href="{href}" target="_blank">Open the Day 1 lab →</a>
</div></div>'''
    return h, note(t, "demo", strip(title_html), ["%s · %s (%s) — %s" % (c, n, m, strip(d)) for c, n, d, m in rows] + ["Success: " + strip(success)], say)


def break_slide(sid, t, minutes, back_at, nxt, label=None, say=None):
    lab = label or f"Break · {minutes} min"
    h = f'''<div class="slide" id="{sid}" data-auto="0" data-min="{minutes}">{BG3}<div class="slide-pad center" style="justify-content:center;align-items:center;text-align:center">
  <div class="topic-eyebrow b in">{lab}</div>
  <div class="tmr b in" data-sec="{minutes*60}" style="margin-top:14px"><div class="tmr-clock">{minutes}:00</div>
   <div class="tmr-back">Scheduled: back at <b>{back_at}</b></div>
   <div class="tmr-ctl"><button data-act="sub" data-d="300">−5</button><button data-act="sub" data-d="60">−1</button><button class="main" data-act="start">Start</button><button data-act="add" data-d="60">+1</button><button data-act="add" data-d="300">+5</button><button data-act="reset">Reset</button></div></div>
  <p class="lead b in" style="margin-top:26px">Next: <b>{nxt}</b></p>
</div></div>'''
    return h, note(t, "pause", lab, ["The timer starts when this slide opens. Back at %s." % back_at, "Next: " + strip(nxt)], say)


def bridge_slide(sid, t, eyebrow, l1, l2, say=None):
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG3}<div class="slide-pad center" style="justify-content:center">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <div class="bridge-l1 b in" style="margin-top:22px">{l1}</div>
  <div class="bridge-l2 b in">{l2}</div>
</div></div>'''
    return h, note(t, "story", eyebrow, [strip(l1), strip(l2)], say)


def ctft_part(sid, t, idx, letter, name, sub, explain, weak, strong, chips_label, chips, rule=None, say=None):
    ch = '<div class="chiprow b in"><span class="cl">%s</span>' % chips_label + "".join(f'<span class="c">{c}</span>' for c in chips) + "</div>"
    rl = f'<div class="keyline b in">{rule}</div>' if rule else ""
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG}<div class="slide-pad">
  <div class="topic-eyebrow b in">CTFT · {idx} of 4 · {name}</div>
  <div class="ctft-head b in"><span class="bigletter">{letter}</span><h2 class="demo-h sm" style="margin:0">{sub}</h2></div>
  <p class="lead b in">{explain}</p>
  <div class="ws b in"><div class="wk"><span class="lab">Weak</span>{weak}</div><div class="st"><span class="lab">Strong</span>{strong}</div></div>
  {ch}{rl}
</div></div>'''
    return h, note(t, "term", "CTFT %d of 4 — %s" % (idx, name), [strip(explain), "Weak: " + strip(weak), "Strong: " + strip(strong)] + ([strip(rule)] if rule else []), say)


def round_slide(sid, t, eyebrow, title_html, sub, parts, quality, verdict, say=None):
    segs = "".join(f'<span class="seg{" new" if new else ""}">{("<span class=\"tag\">" + tag + "</span>") if tag else ""}{H.escape(txt)} </span>' for tag, txt, new in parts)
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <p class="lead b in">{sub}</p>
  <div class="round-p b in">{segs}</div>
  <div class="qmeter b in"><div class="ql"><span>Output quality</span><b>{quality}% · {verdict}</b></div><div class="qt"><div class="qf" style="width:{quality}%"></div></div></div>
</div></div>'''
    return h, note(t, "demo", strip(title_html), [strip(sub), "Run it in Copilot Chat. Quality: %d%% — %s." % (quality, verdict)], say)


def verify_slide(sid, t, eyebrow, title_html, said, real, tip, say=None):
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <div class="vfy b in" data-reveal><div class="say">{said}</div><div class="demo-controls"><button class="btn reveal-btn">Check the source →</button></div><div class="real">{real}</div></div>
  <div class="keyline b in">{tip}</div>
</div></div>'''
    return h, note(t, "check", strip(title_html), ["Copilot says: " + strip(said), "Reality: " + strip(real), strip(tip)], say)


def compare_slide(sid, t, eyebrow, title_html, left, right, cards, say=None):
    cs = "".join(f'<div class="kcard"><div class="kn">{i+1}</div><div class="kt">{c[0]}</div><div class="kd">{c[1]}</div></div>' for i, c in enumerate(cards))
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <div class="wvs b in"><div class="wv-col in"><h4>{left[0]}</h4><p>{left[1]}</p></div><div class="wv-col"><h4>{right[0]}</h4><p>{right[1]}</p></div></div>
  <div class="kcards b in" style="grid-template-columns:repeat(3,1fr)">{cs}</div>
</div></div>'''
    return h, note(t, "term", strip(title_html), [strip(left[0]) + ": " + strip(left[1]), strip(right[0]) + ": " + strip(right[1])] + ["%s — %s" % (strip(a), strip(b)) for a, b in cards], say)


def draw_slide(sid, t, eyebrow, title_html, lead, lesson, say=None):
    shape = ('<svg viewBox="0 0 300 220"><rect x="40" y="110" width="90" height="70" fill="none" stroke="var(--rose)" stroke-width="4"/>'
             '<circle cx="210" cy="80" r="44" fill="none" stroke="var(--rose)" stroke-width="4"/><path d="M130 145 L210 124" stroke="var(--w6)" stroke-width="4"/>'
             '<path d="M150 40 l20 30 h-40z" fill="none" stroke="var(--w6)" stroke-width="4"/></svg>')
    h = f'''<div class="slide" id="{sid}" data-auto="0">{BG2}<div class="slide-pad">
  <div class="topic-eyebrow b in">{eyebrow}</div>
  <h2 class="demo-h sm b in">{title_html}</h2>
  <p class="lead b in">{lead}</p>
  <div class="drawbox b in" data-reveal><div class="shape"><span class="qm">?</span>{shape}</div><button class="btn reveal-btn">Reveal the shape</button></div>
  <div class="keyline b in">{lesson}</div>
</div></div>'''
    return h, note(t, "demo", strip(title_html), [strip(lead), "Show the shape to the volunteer only (open this slide on your laptop first), then reveal to the room.", strip(lesson)], say)
