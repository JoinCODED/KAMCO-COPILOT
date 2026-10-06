import json, re, os, html as H
from deckkit import EX, strip
import labkit
from lab_content import LABS, WELCOME

OUTP = "out/site"; OUTF = "out/facilitator"
CATNAME = {"AI": "Safe use", "PRM": "Prompting", "OUT": "Outlook", "XLS": "Excel", "WRD": "Word", "PPT": "PowerPoint", "AGT": "Agents"}
COPYJS = open(EX + "lab-walkthrough.html", encoding="utf-8").read()
COPYJS = COPYJS[COPYJS.rindex("<script>"):]


def head(example, title):
    s = open(EX + example, encoding="utf-8").read()
    h = s[:s.index("</head>") + 7]
    return re.sub(r"<title>.*?</title>", "<title>%s</title>" % H.escape(title), h)


def bar(brand_html, tabs, tagdemo=False):
    t = "".join(f'<a class="tab" href="#{i}">{l}</a>' for i, l in tabs)
    td = '<span class="tag-demo">facilitation guide</span>' if tagdemo else ""
    return f'<body>\n<div class="bar"><div class="bar-in">\n  <div class="brand"><span class="dot"></span>{brand_html}{td}</div>\n  <div class="tabs">{t}</div>\n</div></div>\n'


def flagchip(f):
    return f'<div class="flag" data-f="{f}"><span class="k">FLAG</span>{f}</div>'


def walkthrough(day, chs):
    tabs = [("c%d" % (i + 1), "%02d %s" % (i + 1, c["title"].split()[0])) for i, c in enumerate(chs)]
    out = head("lab-walkthrough.html", "Day %d Lab · Step-by-Step Solutions — KAMCO Copilot" % day) + bar("Day&nbsp;%d Lab · <b>Step-by-Step Solutions</b>" % day, tabs)
    out += '<main>\n<div class="intro">The %d challenges in the Day %d trainee lab, solved step by step. Each ends in a <b>KAMCO{ }</b> flag the trainee submits to capture it (tap a flag to copy).</div>\n' % (len(chs), day)
    for i, c in enumerate(chs):
        st = "".join(f"<li>{x}</li>" for x in c["sol"]["steps"]) + "<li>All correct → flag reveals.</li>"
        out += (f'<div class="card" id="c{i+1}"><div class="ch-top"><span class="num">{i+1:02d}</span><span class="cat">{CATNAME[c["cat"]]}</span><span class="pts">{c["pts"]} pts · {c["diff"].title()}</span></div>'
                f'<h3>{c["title"]}</h3><div class="scn">{c["scn"]}</div><ol class="steps">{st}</ol>{flagchip(c["data"]["flag"])}'
                f'<div class="point"><span class="ic">◆</span><span class="t">{c["sol"]["point"]}</span></div>'
                + (f'<div class="scn" style="margin-top:12px"><b>⚡ Finished early:</b> {c["extra"]}</div>' if c.get("extra") else "") + '</div>\n')
    out += '</main>\n<div class="foot">Day %d trainee lab (coded-kamco-day-%d-lab.html). The instructor demo lab runs the parallel Al-Waha scenario — see the instructor solutions page.</div>\n' % (day, day)
    return out + COPYJS


def instr_solutions(day, chs):
    tabs = [("c%d" % (i + 1), "%02d %s" % (i + 1, c["title"].split()[0])) for i, c in enumerate(chs)]
    out = head("instructor-solutions.html", "Day %d Instructor Demo · Solutions — KAMCO Copilot" % day) + bar("Day&nbsp;%d Instructor Demo · <b>Solutions</b>" % day, tabs, True)
    out += '<main>\n<div class="intro">The %d demos you run <b>on screen</b> with the Al-Waha scenario — each with the opening line, the steps and the point to land. These mirror the walkthrough inside the instructor lab.</div>\n' % len(chs)
    for i, c in enumerate(chs):
        w = c["walk"]
        st = "".join(f"<li>{x}</li>" for x in w["do"])
        out += (f'<div class="card" id="c{i+1}"><div class="ch-top"><span class="num">{i+1:02d}</span><span class="cat">{CATNAME[c["cat"]]}</span><span class="pts">{c["pts"]} pts</span></div>'
                f'<h3>{c["title"]}</h3><div class="scn">{c["scn"]}</div>'
                f'<div class="say"><span class="ic">▶</span><span class="t"><span class="lbl">Open by saying</span>{w["say"]}</span></div><ol class="steps">{st}</ol>{flagchip(c["data"]["flag"])}'
                f'<div class="point"><span class="ic">◆</span><span class="t"><span class="lbl">Land this</span>{w["point"]}</span></div></div>\n')
    out += '</main>\n<div class="foot">Run these before handing out the trainee lab. Trainee solutions: coded-kamco-day-%d-walkthrough.html.</div>\n' % day
    return out + COPYJS


def answer_key(day, deck, trainee, instr):
    out = head("answer-key.html", "Day %d · Demos & Lab Solutions — KAMCO Copilot" % day) + bar("Day&nbsp;%d · <b>Demos & Lab Solutions</b>" % day, [("demos", "▶ Demos"), ("checks", "✓ Mini-checks"), ("lab", "⚑ Trainee lab"), ("instr", "🎬 Instructor lab")])
    demos = [n for n in deck["notes"] if n["k"] == "demo" and n["h"].startswith("Live demo")]
    out += '<main>\n<section id="demos"><div class="sec-h"><h2>Demos you run live</h2><span class="c">%d in-deck</span></div><div class="sec-sub">The interactive and live-in-Copilot slides — what to run and the point to land.</div>\n' % len(demos)
    for n in demos:
        out += f'<div class="card"><span class="tag">{n["t"].upper()}</span><h3>{n["h"].replace("Live demo — ", "")}</h3><div class="sol"><span class="ar">→</span><div class="txt"><ol>' + "".join(f"<li>{b}</li>" for b in n["b"]) + "</ol></div></div></div>\n"
    out += '</section>\n<section id="checks"><div class="sec-h"><h2>Mini-check answers</h2><span class="c">"your call"</span></div><div class="sec-sub">The correct answer for every "your call" slide.</div><div class="checks">'
    for c in deck["checks"]:
        out += f'<div class="chk"><div class="q"><b>Slide {c["slide"]}</b> · {H.escape(c["q"])}</div><div class="a">{H.escape(c["a"])}</div></div>'
    out += '</div></section>\n<section id="lab"><div class="sec-h"><h2>Trainee lab — solutions</h2><span class="c">%d challenges</span></div><div class="sec-sub">Flag format <span style="font-family:var(--mono);color:var(--rose-lt)">KAMCO{ }</span> — tap a flag to copy.</div>\n' % len(trainee)
    for i, c in enumerate(trainee):
        out += f'<div class="card lab"><span class="tag">{i+1:02d} · {CATNAME[c["cat"]]}</span><h3>{c["title"]}</h3>{flagchip(c["data"]["flag"])}<div class="solve">' + " ".join(strip_tags_keep(c["sol"]["steps"])) + "</div></div>\n"
    out += '</section>\n<section id="instr"><div class="sec-h"><h2>Instructor demo lab</h2><span class="c">flags</span></div><div class="sec-sub">The parallel Al-Waha challenges you run on screen.</div><div class="instr-flags">'
    out += "".join(f'<span class="f">{c["data"]["flag"]}</span>' for c in instr)
    out += '</div></section>\n</main>\n<div class="foot">Slide-by-slide talking points: coded-kamco-day-%d-notes.html. Step-by-step lab solutions: coded-kamco-day-%d-walkthrough.html.</div>\n' % (day, day)
    ak = open(EX + "answer-key.html", encoding="utf-8").read()
    return out + ak[ak.rindex("<script>"):]


def strip_tags_keep(steps):
    return steps


if __name__ == "__main__":
    for day in (1, 2):
        for mode in ("trainee", "instructor"):
            chs = LABS[(mode, day)]
            title = ("Day %d — KAMCO Copilot Lab" if mode == "trainee" else "Day %d · Instructor — KAMCO Copilot Lab") % day
            fn = ("coded-kamco-day-%d-lab.html" if mode == "trainee" else "coded-kamco-day-%d-instructor-lab.html") % day
            html = labkit.lab_page(mode, day, WELCOME[(mode, day)], chs, title)
            open(os.path.join(OUTP if mode == "trainee" else OUTF, fn), "w", encoding="utf-8").write(html)
        deck = json.load(open("out/deck%d.json" % day))
        open(os.path.join(OUTF, "coded-kamco-day-%d-walkthrough.html" % day), "w", encoding="utf-8").write(walkthrough(day, LABS[("trainee", day)]))
        open(os.path.join(OUTF, "coded-kamco-day-%d-instructor-solutions.html" % day), "w", encoding="utf-8").write(instr_solutions(day, LABS[("instructor", day)]))
        open(os.path.join(OUTF, "coded-kamco-day-%d-answer-key.html" % day), "w", encoding="utf-8").write(answer_key(day, deck, LABS[("trainee", day)], LABS[("instructor", day)]))
        print("day", day, "built")
