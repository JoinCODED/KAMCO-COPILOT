"""Lab builder: splices the KIBS gold-standard lab (CSS + engines + shell) and injects KAMCO data.
Adds one engine ('answer': type the figure you found in Copilot/Excel) and parametrises three existing ones."""
import json, re
from deckkit import EX

T = open(EX + "trainee-lab.html", encoding="utf-8").read()
_s = T.index("<script>")
CSS_HEAD = T[:_s]
_code = T.index("function md5")
ENGINE = T[_code:T.rindex("</script>")]

CSS_HEAD = CSS_HEAD.replace("family=JetBrains+Mono:wght@400;500;700", "family=Space+Mono:wght@400;700")
CSS_HEAD = CSS_HEAD.replace("--mono:'JetBrains Mono',ui-monospace,monospace", "--mono:'Space Mono',ui-monospace,monospace")
CSS_HEAD = CSS_HEAD.replace("</style></head><body>", """
/* KAMCO categories + answer engine (lab tokens) */
.cdot.AI,.cdot.PRM{background:var(--violet)}.cdot.OUT,.cdot.AGT{background:var(--blue)}.cdot.XLS{background:var(--amber)}.cdot.WRD,.cdot.PPT{background:var(--rose)}
.badge.cat-AI,.badge.cat-PRM{color:var(--violet);border-color:rgba(160,122,230,.42)}.badge.cat-OUT,.badge.cat-AGT{color:var(--blue);border-color:rgba(74,135,232,.42)}
.badge.cat-XLS{color:var(--amber);border-color:rgba(234,185,74,.42)}.badge.cat-WRD,.badge.cat-PPT{color:var(--rose-lt);border-color:rgba(230,107,130,.42)}
.ans-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap;padding:0 16px 14px}
.ans-row .sb-in{max-width:280px}
.ans-unit{font-family:var(--mono);font-size:13px;color:var(--faint)}
.ans-src{display:inline-block;margin-top:4px;font-size:13.5px;color:var(--dim)}.ans-src a{color:var(--rose-lt)}
.ec-mail{white-space:pre-wrap;font-size:14px;line-height:1.6;color:var(--ink2);max-height:340px;overflow:auto;padding:14px 16px;border:1px solid var(--line);border-radius:var(--r);background:rgba(0,0,0,.25);margin-bottom:14px}
.ec-mail details summary{cursor:pointer}
.st-intro a{color:var(--rose-lt)}
.xtra{margin-top:12px;padding:12px 14px;border:1px dashed var(--line2);border-radius:var(--r);font-size:14px;color:var(--ink2);background:rgba(74,135,232,.06)}.xtra b{color:var(--blue)}
</style></head><body>""")
CSS_HEAD = re.sub(r"<title>.*?</title>", "<title>__TITLE__</title>", CSS_HEAD, count=1)

# --- shell text: KIBS -> KAMCO / CODED ---
E = ENGINE
E = E.replace("""'<div class="brand"><img class="klogo" src="'+KIBS_LOGO+'" alt="KIBS — Kuwait Institute of Banking Studies"><div class="bt">KIBS<b>Cyber Lab</b></div></div>'""",
              """'<div class="brand"><div class="mark">C</div><div class="bt">KAMCO<b>Copilot Lab</b></div></div>'""")
E = E.replace("""'<div class="wrap"><div class="hero"><div class="cobrand"><img class="kbig" src="'+KIBS_LOGO+'" alt="KIBS — Kuwait Institute of Banking Studies"><div class="cb-txt"><b>Kuwait Institute of Banking Studies</b><span>Technology &amp; Information Risk Management</span></div></div>""",
              """'<div class="wrap"><div class="hero"><div class="cobrand"><div class="cb-txt"><b>CODED × KAMCO Invest</b><span>AI at Work with Microsoft Copilot</span></div></div>""")
E = E.replace("STORE='kibs_'+DAYNO+'_'+MODE", "STORE='kamco_'+DAYNO+'_'+MODE")
E = E.replace("href=\"coded-kibs-day-'+DAYNO+'.html\"", "href=\"coded-kamco-day-'+DAYNO+'.html\"")
E = E.replace("flag · <b>KIBS{ }</b>", "flag · <b>KAMCO{ }</b>")
E = E.replace("Work the <b>live environment</b> — read the inbox, run the terminal, hunt the logs, judge the call. ",
              "Work it for real — in the lab, and in <b>Copilot</b> with your Al-Murjan files. When a challenge asks for a figure, enter what you found. ")
E = E.replace("'Everything is safe, in-browser, and benign.'", "'All client data is fictional.'")
E = E.replace("Uncover the <b>KIBS{…} flag</b>", "Uncover the <b>KAMCO{…} flag</b>")
E = E.replace("<b>KIBS{…}</b> flag", "<b>KAMCO{…}</b> flag")
E = E.replace('placeholder="KIBS{ … }"', 'placeholder="KAMCO{ … }"')
E = E.replace('Flag format <span class="pill">KIBS{ ___ }</span>', 'Flag format <span class="pill">KAMCO{ ___ }</span>')
assert "KIBS" not in E.replace("KIBS_LOGO", ""), [m.start() for m in re.finditer("KIBS", E)][:5]

# --- parametrise engines ---
E = E.replace("'<div class=\"inbox\" id=\"inbox\"><div class=\"mlist\"><div class=\"mhd\">INBOX · 5 unread · <span id=\"triaged\">0</span>/5 triaged</div>",
              "(data.intro?'<div class=\"st-intro\">'+data.intro+'</div>':'')+'<div class=\"inbox\" id=\"inbox\"><div class=\"mlist\"><div class=\"mhd\">INBOX · '+M.length+' unread · <span id=\"triaged\">0</span>/'+M.length+' sorted</div>")
E = E.replace("if(ans<5){h.textContent='Triage all 5 first — '+(5-ans)+' left.';return;}var ok=0;state.forEach(function(s,i){if(s.v===M[i].key)ok++;});\n    if(ok===5){h.textContent='';done();}else h.textContent=ok+'/5 correct. Re-check the domain, the pressure, the ask.';};",
              "if(ans<M.length){h.textContent='Sort all '+M.length+' first — '+(M.length-ans)+' left.';return;}var ok=0;state.forEach(function(s,i){if(s.v===M[i].key)ok++;});\n    if(ok===M.length){h.textContent='';done();}else h.textContent=ok+'/'+M.length+' correct. '+(data.failMsg||'Re-check.');};")
assert "data.failMsg" in E
E = E.replace("'<div class=\"st-actions\"><button class=\"btn check\">Submit the 3 tells →</button>", "'<div class=\"st-actions\"><button class=\"btn check\">'+(data.btn||'Submit the 3 tells →')+'</button>")
assert "data.btn" in E
E = E.replace("id=\"hb\" style=\"margin-top:10px\">▾ View full headers</button>'", "id=\"hb\" style=\"margin-top:10px\">'+(data.hbtn||'▾ View full headers')+'</button>'")
assert "data.hbtn" in E
_w = """'<div class="wild"><b>⚑ Seen in the wild —</b> '+c.wild+'</div>'+"""
assert _w in E
E = E.replace(_w, _w + """(c.extra&&MODE==='trainee'?'<div class="xtra"><b>⚡ Finished early?</b> '+c.extra+'</div>':'')+""")
assert E.rstrip().endswith("initShell();"), E[-80:]
E = E.rstrip() + "\n(function(){var h=(location.hash||'').slice(1);if(h&&byId(h))openChallenge(h);})();\n"
E = E.replace("<p class=\"ir-prompt\">You ran the full loop in order: detect, contain, eradicate, recover, learn — without making it worse.</p>'",
              "<p class=\"ir-prompt\">'+(data.doneMsg||'All steps done in order.')+'</p>'")
assert "data.doneMsg" in E
E = E.replace("'<div class=\"ir-stage\">", "(data.intro?'<div class=\"st-intro\">'+data.intro+'</div>':'')+'<div class=\"ir-stage\">")
E = E.replace("root.innerHTML='<div class=\"inbox\" style=\"grid-template-columns:1fr\">", "root.innerHTML=(data.intro?'<div class=\"st-intro\">'+data.intro+'</div>':'')+'<div class=\"inbox\" style=\"grid-template-columns:1fr\">")

ANSWER = r"""
/* ============ answer (enter the figure you found) ============ */
function buildAnswer(root,done,data){
  root.innerHTML='<div class="st-intro">'+data.intro+'</div>'+(data.mail?'<div class="ec-mail">'+data.mail+'</div>':'')+'<div class="items"></div>'+
   '<div class="st-actions"><button class="btn check">Check my answers →</button><button class="btn ghost reset">Reset</button><span class="st-hint"></span></div>';
  var box=root.querySelector('.items'),sel={};
  data.fields.forEach(function(f,i){var c=document.createElement('div');c.className='it-card';
    var ctl=f.kind==='select'?'<div class="it-opts">'+f.opts.map(function(o,j){return '<button class="opt" data-k="'+j+'">'+o+'</button>';}).join('')+'</div>'
      :'<div class="ans-row"><input class="sb-in" type="text" inputmode="decimal" autocomplete="off" placeholder="'+(f.ph||'your answer')+'"><span class="ans-unit">'+(f.unit||'')+'</span></div>';
    c.innerHTML='<div class="it-body">'+f.label+'</div>'+ctl+'<div class="it-fb"></div>';box.appendChild(c);
    c.querySelectorAll('.opt').forEach(function(b){b.onclick=function(){sel[i]=+b.dataset.k;c.querySelectorAll('.opt').forEach(function(x){x.classList.toggle('on',x===b);});};});});
  function num(v){v=String(v||'').replace(/kwd|%|,|\s/gi,'');return v===''?NaN:parseFloat(v);}
  root.querySelector('.check').onclick=function(){var ok=0,miss=0;data.fields.forEach(function(f,i){var c=box.children[i],fb=c.querySelector('.it-fb'),g;
      if(f.kind==='select'){if(sel[i]==null){miss++;return;}g=sel[i]===f.answer;}
      else{var v=num(c.querySelector('input').value);if(isNaN(v)){miss++;return;}g=Math.abs(v-f.answer)<=(f.tol||0);}
      if(g)ok++;c.classList.toggle('good',g);c.classList.toggle('bad',!g);fb.className='it-fb show '+(g?'g':'b');fb.innerHTML=(g?'✓ ':'✗ ')+(g?(f.why||'Correct.'):(f.hint||'Not yet — check your work in Excel and try again.'));});
    var h=root.querySelector('.st-hint');if(miss){h.textContent='Answer all '+data.fields.length+' first.';return;}
    if(ok===data.fields.length){h.textContent='';done();}else h.textContent=ok+'/'+data.fields.length+' correct — fix the red ones.';};
  root.querySelector('.reset').onclick=function(){reopenChallenge(data.resetId);};
}
"""
E = E.replace("var ENGINES={assign:buildAssign,", ANSWER + "\nvar ENGINES={answer:buildAnswer,assign:buildAssign,")


def lab_page(mode, day, welcome, challenges, title):
    flags = {c["id"]: c["data"]["flag"] for c in challenges}
    clean = []
    for c in challenges:
        d = {k: v for k, v in c.items() if k not in ("sol",)}
        if mode == "trainee":
            d.pop("walk", None)
        clean.append(d)
    data = ('var MODE=%s;var DAYNO=%d;var DAYLABEL=%s;var KIBS_LOGO="";var WELCOME=%s;var FLAGS=%s;var CHALLENGES=%s;\n'
            % (json.dumps(mode), day, json.dumps("Day %d" % day), json.dumps(welcome, ensure_ascii=False), json.dumps(flags, ensure_ascii=False), json.dumps(clean, ensure_ascii=False)))
    return CSS_HEAD.replace("__TITLE__", title) + "<script>" + data + E + "</script></body></html>"
