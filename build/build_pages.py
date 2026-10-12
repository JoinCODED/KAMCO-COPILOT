import re, os, json, html as H, shutil
from deckkit import EX
from emails import MURJAN_THREAD, thread_text

_lp = EX + "coded-logo.txt"
if not os.path.exists(_lp):
    _lp = EX.rsplit("references/", 1)[0] + "assets/coded-logo.txt"
LOGO = open(_lp).read().strip()
if not LOGO.startswith("data:"):
    LOGO = "data:image/png;base64," + LOGO
OUTP = "out/site"
A = json.load(open("out/answers.json"))

ICAL = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="3" y="4.5" width="18" height="17" rx="2.5"/><path d="M16 2.5v4M8 2.5v4M3 10h18"/></svg>'
ICLK = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7.5v5l3 2"/></svg>'
IPIN = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10.5c0 6.5-9 12.5-9 12.5s-9-6-9-12.5a9 9 0 0118 0z"/><circle cx="12" cy="10.5" r="3"/></svg>'
ICHK = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12l5 5L20 6"/></svg>'
ICUP = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h13v5a5 5 0 01-5 5H9a5 5 0 01-5-5z"/><path d="M17 9h2a2.5 2.5 0 010 5h-2"/></svg>'
ILINK = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10 13a5 5 0 007 0l2-2a5 5 0 00-7-7l-1 1"/><path d="M14 11a5 5 0 00-7 0l-2 2a5 5 0 007 7l1-1"/></svg>'
IOUT = '<svg class="out" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M8 7h9v9"/></svg>'
ISCREEN = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8M12 17v4"/></svg>'
IFLAG = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>'
IFILE = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6a2 2 0 00-2 2v14a2 2 0 002 2h12a2 2 0 002-2V9z"/><path d="M14 3v6h6"/></svg>'


def head(example, title, extra_css=""):
    s = open(EX + example, encoding="utf-8").read()
    h = s[:s.index("</head>")]
    h = re.sub(r"<title>.*?</title>", "<title>%s</title>" % H.escape(title), h)
    return h + extra_css + "</head>\n"


# ---------------- day pages ----------------
DAYS = {
 1: dict(title="From Inbox to Insight", cat="Day 1 · Request → Check", date="Sun 11 Oct 2026",
    lede="Read a messy client thread with Copilot in Outlook, find the real ask, then clean and analyse the Al-Murjan custody export in Excel — and check it against the mandate.",
    brief="Every KAMCO request follows the same path: an email arrives, the data gets checked, an output gets produced, and a reply goes out. Today covers the first half. You will learn what Copilot can and cannot do, write prompts that work for investment tasks, find the deadline and the deliverable in a long thread, and turn a messy custody export into a clean analysis you can explain line by line.",
    ros=[("MAP test — your starting point", "09:00", "30 minutes, alone. <a href='https://portal.joincoded.com/sv/kamco-copilot-map-test-pre-day-1' target='_blank' rel='noopener'>Open the MAP test ↗</a>"),
         ("Block 1 — What is AI? What is an LLM? Meet Copilot", "09:30", "Ice breaker, setup check, AI → LLM → how it answers, Copilot, Work vs Web, safe use. Lab 1."), ("brk", "10:20", "Break"),
         ("Block 2 — Prompting with CTFT", "10:30", "Describe the drawing, the four ingredients, zero to hero in four rounds. Lab 2."), ("brk", "11:20", "Break"),
         ("Block 3 — Read the request in Outlook", "11:30", "Summarise the thread, extract the ask, draft a holding reply. Labs 3–4."), ("brk", "12:00", "Lunch"),
         ("Block 4 — Excel: clean the data", "13:00", "Duplicates, text numbers, missing prices, messy labels. Lab 5."), ("brk", "13:50", "Break"),
         ("Block 5 — Excel: find the story", "14:00", "Allocation vs mandate, the issuer limit, contributors. Labs 6–7."), ("brk", "14:50", "Break"),
         ("Hands-on — the Al-Murjan request, alone", "15:00", "From the email to a clean, checked analysis. Instructors observe."),
         ("Recap & close", "15:50", "Back to the ice-breaker wall. Save your file in OneDrive — you need it tomorrow.")],
    leave=["Use Copilot safely with client data, with your work account.", "Write prompts with Context, Task, Format and Tone.", "Find the real deadline and deliverable in a long thread.", "Clean a custody export and check it against a mandate.", "Explain every number you produce."],
    chips=["What is AI?", "LLMs", "Copilot Chat", "Work vs Web", "CTFT prompts", "Outlook Summarise", "Excel cleaning", "PivotTables", "Mandate check", "Issuer limit"],
    lab="Nine tasks, in the order of the day: first contact, your time audit, safe or not, from zero to hero, build your own prompt, tame the thread, and three Excel tasks on the Al-Murjan export. Each has a Stretch and a Boss challenge for early finishers."),
 2: dict(title="From Insight to Output", cat="Day 2 · Produce → Automate → Prove it", date="Mon 12 Oct 2026",
    lede="Write in Word, present in PowerPoint, reuse prompts and build your own agent — then complete one full request alone, in your own field.",
    brief="Today Copilot works inside Word and PowerPoint: notes become a memo, the house view becomes a client deck. You then find and adapt ready-made prompts in the Prompt Gallery, build a Request Triage Assistant agent and test it, After lunch you complete one full request alone in your own field — the graded capstone — then take the end MAP test, fill in the survey and receive your certificate.",
    ros=[("Block 1 — Word", "09:00", "Draft, rewrite, ground in the house view, check. Lab E2.1."), ("brk", "09:50", "Break"),
         ("Block 2 — PowerPoint", "10:00", "Create a deck from a file, add a slide, check it. Labs E2.2–E2.3."), ("brk", "10:50", "Break"),
         ("Block 3 — Prompt libraries + Agents", "11:00", "The Prompt Gallery and your own library in Word; a built-in agent, then build your own. Labs E2.4–E2.7."), ("brk", "12:00", "Lunch"),
         ("Capstone — graded", "13:00", "Pick your field — Wealth Management, Asset Management, Operations or Investment Research. Email → clean → analyse → chart → executive brief → deck → reply by 2:50 pm. Lab E2.8."), ("brk", "14:50", "Break"),
         ("MAP test — see your progress", "15:00", "30 minutes, alone. <a href='https://portal.joincoded.com/sv/kamco-copilot-map-test-post-day-2' target='_blank' rel='noopener'>Open the MAP test ↗</a>"),
         ("Certificates & close", "15:30", "<a href='https://portal.joincoded.com/sv/kamco-copilot-end-of-program-satisfaction-survey' target='_blank' rel='noopener'>Satisfaction survey ↗</a>, then certificates by name and the link to Program 3.")],
    leave=["Turn notes into a memo in Word — and ground it in a file.", "Create a client deck from a document in PowerPoint, and check it.", "Find and adapt Gallery prompts — and keep your own library in Word.", "Use a built-in agent, then build, test and fix your own.", "Check AI work for accuracy, confidentiality, tone and completeness before you send it."],
    chips=["Copilot in Word", "Copilot in PowerPoint", "Prompt Gallery", "Prompt library", "Built-in agents", "Agent Builder", "Four checks", "Capstone"],
    lab="Nine tasks: notes to memo, house view to deck, message titles, the Prompt Gallery, your own prompt library in Word, a built-in agent, build your own agent, the graded capstone in your own field, and the MAP test and survey. Each has a Stretch or Boss challenge for early finishers."),
}


def day_page(n):
    d = DAYS[n]; o = 3 - n
    css = '<style>.d-hero h1{max-width:900px}.res-list .res-tag{white-space:nowrap}</style>'
    out = head("day-page.html", "Day %d · %s — KAMCO Copilot" % (n, d["title"]), css) + "<body>\n"
    out += '<div class="wrap"><div class="topbar"><a class="back" href="index.html"><span class="ar">←</span> Back to the programme</a></div></div>\n'
    out += f'''<div class="wrap hero-wrap"><div class="d-hero h-d{n}"><div class="d-hero-top"><span class="cat-pill"><span class="dot"></span> {d["cat"]}</span></div>
<h1>{d["title"]}</h1><p class="lede">{d["lede"]}</p>
<div class="d-meta"><span>{ICAL} {d["date"]}</span><span>{ICLK} 09:00 – 16:00</span><span>{IPIN} CODED Campus, Kuwait</span></div></div></div>\n'''
    ros = ""; k = 0
    for t, tm, desc in d["ros"]:
        if t == "brk":
            ros += f'<li class="is-brk"><span class="brk">{ICUP}</span><div class="rc"><div class="rt"><b>{desc}</b><span class="time">{tm}</span></div></div></li>\n'
        else:
            k += 1
            ros += f'<li><span class="num">{k}</span><div class="rc"><div class="rt"><b>{t}</b><span class="time">{tm}</span></div><div class="rd">{desc}</div></div></li>\n'
    leave = "".join(f"<li>{ICHK}<span>{x}</span></li>" for x in d["leave"])
    chips = "".join(f'<span class="chip2">{c}</span>' for c in d["chips"])
    res = [("coded-kamco-day-%d-deck.html" % n, "Day %d slide deck" % n, "Slides"), ("coded-kamco-day-%d-lab.html" % n, "Day %d hands-on lab" % n, "Lab"),
           ("case-files.html", "Case files — emails & Excel", "Files"), ("before-you-start.html", "Before you start — sign-in & backup", "Setup"),
           ("cheat-sheet.html", "Copilot cheat sheet", "Reference"), ("coded-kamco-day-%d.html" % o, "Day %d · %s" % (o, DAYS[o]["title"]), "Day plan"), ("index.html", "The programme", "Overview")]
    resh = "".join(f'<a class="res" href="{h}"><span class="res-ic">{ILINK}</span><span class="res-nm">{l}</span><span class="res-tag">{t}</span>{IOUT}</a>\n' for h, l, t in res)
    out += f'''<div class="wrap"><div class="d-grid"><div class="d-main">
<section class="panel"><h2>Workshop brief</h2><p class="brief">{d["brief"]}</p></section>
<section class="panel"><h2>Run of show</h2><p class="muted">50-minute sessions, 10-minute breaks, lunch 12:00 – 13:00.</p><ol class="ros">
{ros}</ol></section></div>
<aside class="d-side">
<section class="panel"><h3>What you will be able to do</h3><ul class="leave">{leave}</ul></section>
<section class="panel"><h3>What we will cover</h3><div class="chips">{chips}</div></section>
<section class="panel cta-panel"><div class="cta-ico">{ISCREEN}</div><h3>Day {n} slides</h3><p>The full interactive deck — the stories, the live demos and the exact prompts, as run in the room.</p><a class="slides-btn" href="coded-kamco-day-{n}-deck.html"><span>Open the slides</span> <span class="ar">→</span></a></section>
<section class="panel cta-panel"><div class="cta-ico">{IFLAG}</div><h3>Day {n} hands-on lab</h3><p>{d["lab"]}</p><a class="slides-btn" href="coded-kamco-day-{n}-lab.html"><span>Open the lab</span> <span class="ar">→</span></a></section>
<section class="panel cta-panel"><div class="cta-ico">{IFILE}</div><h3>Case files</h3><p>The Al-Murjan email thread, the 30 Sep custody export and the house view. Save them to your OneDrive before you start.</p><a class="slides-btn" href="case-files.html"><span>Open the case files</span> <span class="ar">→</span></a></section>
<section class="panel"><h3>Resources &amp; links</h3><div class="res-list">
{resh}</div></section>
</aside></div></div>
<footer class="site-foot"><div class="wrap"><div class="foot-row"><span class="copy">AI at Work with Microsoft Copilot · CODED × KAMCO Invest</span><span class="copy">© 2026 CODED · Kuwait</span></div></div></footer>
</body></html>'''
    return out


# ---------------- landing ----------------
def landing():
    s = open(EX + "landing.html", encoding="utf-8").read()
    h = re.sub(r"<title>.*?</title>", "<title>AI at Work with Microsoft Copilot — CODED × KAMCO Invest</title>", s[:s.index("</head>")])
    h += '<style>.lockup .ptxt,.f-lockup .ptxt{font-weight:800;letter-spacing:-.3px;color:var(--ink);font-size:20px}.f-lockup .ptxt{font-size:16px}</style></head>\n'

    def card(n, cat, icon, chip_time, title, tag, desc, items):
        li = "".join(f"<li>{ICHK} {x}</li>" for x in items)
        return f'''<article class="pcard"><div class="phead h-d{n}"><span class="cat">{cat}</span><span class="head-icon">{icon}</span>
<div class="head-meta"><span class="chip">{ICAL.replace('15','13')} Day {n}</span><span class="chip">{ICLK.replace('15','13')} {chip_time}</span></div></div>
<div class="pbody"><div class="kicker">Day 0{n}</div><h3>{title}</h3><div class="tagline">{tag}</div><p class="pdesc">{desc}</p><ul class="plist">{li}</ul>
<a href="coded-kamco-day-{n}.html" class="pbtn btn-d{n}">Open day {n} <span class="arr">→</span></a></div></article>'''
    i1 = '<svg viewBox="0 0 24 24" width="42" height="42" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>'
    i2 = '<svg viewBox="0 0 24 24" width="42" height="42" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M22 2L11 13"/><path d="M22 2l-7 20-4-9-9-4z"/></svg>'
    body = f'''<body>
<header class="hero"><div class="glow g1"></div><div class="glow g2"></div><div class="glow g3"></div><div class="glow g4"></div>
<div class="inner"><div class="pill"><span class="dot"></span> CODED × KAMCO Invest · Kuwait</div>
<div class="lockup"><img class="coded-logo" src="{LOGO}" alt="CODED"><span class="x">×</span><span class="ptxt">KAMCO Invest</span></div>
<h1 class="headline">AI at Work with<br><span class="accent">Microsoft Copilot</span></h1>
<p class="sub">A two-day, hands-on program for KAMCO Invest. One real investment request, followed through Outlook, Excel, Word and PowerPoint — from the first email to a reply you can stand behind.</p>
<div class="meta"><span>{ICAL.replace('15','16')} Sun 11 – Mon 12 Oct 2026</span><span>{IPIN.replace('15','16')} CODED Campus, Kuwait</span></div>
<a href="#programme" class="cta">Explore the programme <span class="arr">→</span></a></div><div class="scrollhint">the two days ↓</div></header>
<section class="programme" id="programme"><div class="wrap"><div class="eyebrow">The programme</div>
<h2 class="sec-title">Two days, one workflow.</h2>
<p class="sec-lead">Request → Check → Produce → Reply. Day one takes a client request from a messy email thread to a clean, checked analysis. Day two puts Copilot to work in Word and PowerPoint, adds prompt libraries and agents — then you do a full request alone, in your own field, for the graded capstone.</p>
<div class="cards">
{card(1, "Request → Check", i1, "09:00 – 16:00", "From Inbox to Insight", "Outlook and Excel", "Find the real ask in a long thread, then clean and analyse a custody export against the client's mandate.", ["Use Copilot safely with client data", "Prompt with Context, Task, Format and Tone", "Clean the data and check the mandate in Excel"])}
{card(2, "Produce → Automate", i2, "09:00 – 16:00", "From Insight to Output", "Word, PowerPoint, prompt libraries and agents", "Write and present with Copilot, build your own agent — and complete one full request alone, in your own field.", ["Notes to memo in Word, house view to deck in PowerPoint", "Prompt libraries, built-in agents and your own agent", "A graded capstone in your field"])}
</div></div></section>
<footer class="site-foot"><div class="wrap"><div class="foot-top"><div class="foot-brand"><div class="f-lockup"><img class="coded-logo" src="{LOGO}" alt="CODED"><span class="x">×</span><span class="ptxt">KAMCO Invest</span></div>
<p>AI at Work with Microsoft Copilot — a hands-on program run by CODED for KAMCO Invest, Kuwait. All client names and figures in the exercises are fictional.</p></div>
<div class="foot-cols"><div class="foot-col"><h4>Explore</h4><a href="#programme">The programme</a><a href="coded-kamco-day-1.html">Day 1 · From Inbox to Insight</a><a href="coded-kamco-day-2.html">Day 2 · From Insight to Output</a></div>
<div class="foot-col"><h4>Resources</h4><a href="before-you-start.html">Before you start</a><a href="case-files.html">Case files</a><a href="cheat-sheet.html">Cheat sheet</a></div></div></div>
<div class="foot-divider"></div><div class="foot-bottom"><span>© 2026 CODED. Built with care.</span><span>Sun 11 – Mon 12 Oct 2026 · Kuwait</span></div></div></footer>
</body></html>'''
    return h + body


# ---------------- simple panel pages (case files, before you start) ----------------
def panel_page(title, cat, h1, lede, panels):
    css = '<style>.mailtxt{white-space:pre-wrap;font-size:14px;line-height:1.65;color:var(--ink-dim);background:rgba(0,0,0,.25);border:1px solid var(--line);border-radius:12px;padding:16px 18px;max-height:520px;overflow:auto}.steps2{margin:12px 0 0 20px;color:var(--ink-dim);line-height:1.7;font-size:14.5px}.steps2 b{color:var(--ink)}.panel p{color:var(--ink-dim);line-height:1.6;font-size:14.5px;margin-top:8px}.panel p b{color:var(--ink)}.one-col{max-width:880px;margin:0 auto}</style>'
    out = head("day-page.html", title, css) + "<body>\n"
    out += '<div class="wrap"><div class="topbar"><a class="back" href="index.html"><span class="ar">←</span> Back to the programme</a></div></div>\n'
    out += f'<div class="wrap hero-wrap"><div class="d-hero h-d1"><div class="d-hero-top"><span class="cat-pill"><span class="dot"></span> {cat}</span></div><h1>{h1}</h1><p class="lede">{lede}</p></div></div>\n<div class="wrap"><div class="one-col">\n'
    for ph, pb in panels:
        out += f'<section class="panel"><h2>{ph}</h2>{pb}</section>\n'
    out += '</div></div>\n<footer class="site-foot"><div class="wrap"><div class="foot-row"><span class="copy">AI at Work with Microsoft Copilot · CODED × KAMCO Invest</span><span class="copy">All client data is fictional</span></div></div></footer></body></html>'
    return out


def res(h, l, t):
    return f'<a class="res" href="{h}" download><span class="res-ic">{ILINK}</span><span class="res-nm">{l}</span><span class="res-tag">{t}</span>{IOUT}</a>'


def case_files():
    m = A["murjan"]
    return panel_page("Case files — KAMCO Copilot", "Case files · Al-Murjan Family Office", "The Al-Murjan request",
        "Everything you need for the Day 1 and Day 2 exercises. Save the files to your OneDrive first — Copilot in Excel, Word and PowerPoint works on files saved there.",
        [("1 · The email thread", "<p>Your instructor sends this thread to your KAMCO inbox at the start of Day 1. If it does not arrive, open the .eml file below, or read it here and paste it into Copilot Chat.</p>"
          f'<div class="mailtxt">{H.escape("Subject: " + MURJAN_THREAD["subject"] + chr(10) + "Attachment: " + MURJAN_THREAD["attach"] + chr(10) + chr(10) + thread_text(MURJAN_THREAD))}</div>'),
         ("2 · Files to download", '<div class="res-list">' + res(m["file"], "Al-Murjan custody export · 30 Sep 2026 (Excel)", "Excel") + res("01-amfo-q3-review-request.eml", "The email thread (.eml, opens in Outlook)", "Email")
          + res("house-view-q4-2026.docx", "Investment House View · Q4 2026 (Word)", "Word") + res("my-prompt-library.docx", "My Prompt Library · template (Word)", "Word") + "</div>"),
         ("3 · How to set up the Excel file", '<ol class="steps2"><li>Save <b>' + m["file"] + '</b> to your <b>OneDrive</b> and open it in Excel. Turn <b>AutoSave</b> on.</li><li>Delete rows 1–3 above the headers. Click inside the data and press <b>Ctrl+T</b> to make it a table.</li><li>Open Copilot in Excel and follow the prompts from the deck. Check the row count after every step.</li><li>Keep the file. You need it on Day 2 for the memo, the deck and the reply.</li></ol>'),
         ("Good to know", "<p>All clients, people, companies and prices are <b>fictional</b>, created for this training. The project files for Day 2 arrive by email at 13:30.</p>")])


def before_you_start():
    return panel_page("Before you start — KAMCO Copilot", "Setup · 5 minutes", "Before you start",
        "Check that Copilot works on your laptop before Day 1 begins. If something is missing, there is a fallback for every exercise.",
        [("1 · Sign in", '<ol class="steps2"><li>Open <b>copilot.cloud.microsoft</b> (or m365copilot.com) and sign in with your <b>KAMCO work account</b>.</li><li>Type <b>Hello</b> and press Enter. An answer back? You are ready.</li><li>Open Outlook, Excel, Word and PowerPoint and look for the <b>Copilot</b> button on the ribbon.</li></ol>'),
         ("2 · No licence, or Copilot is missing?", "<p>Tell your instructor straight away. CODED has <b>backup accounts with Copilot</b> for the training. Your instructor gives you a sign-in on the day — do not use a personal account for work data.</p>"),
         ("3 · Fallbacks if one app has no Copilot", '<ol class="steps2"><li><b>Outlook:</b> paste the email thread into Copilot Chat and use the same prompt.</li><li><b>Excel:</b> upload the workbook to Copilot Chat and ask for the calculation with the numbers shown, so you can check them.</li><li><b>Word:</b> draft in Copilot Chat, then paste into Word.</li><li><b>PowerPoint:</b> ask Copilot Chat for a 5-slide outline with titles, bullets and speaker notes.</li></ol>'),
         ("4 · Rules for this training", '<ol class="steps2"><li>Use your <b>work account</b> only.</li><li>Use only the <b>training files</b> — never real client data.</li><li>Save files to <b>OneDrive</b> with AutoSave on (needed for Copilot in Excel).</li><li>Copilot drafts. <b>You decide</b> — check every number.</li></ol>'),
         ("5 · Copilot Agent Builder", "<p>On Day 2 the instructor builds an agent live. If Agent Builder is switched on for your account, you can follow along: Microsoft 365 Copilot app → <b>Agents</b> → <b>Create agent</b>. If it is switched off, you watch the demo — nothing in the project depends on it.</p>")])


# ---------------- cheat sheet ----------------
def cheat():
    s = open(EX + "cheat-sheet.html", encoding="utf-8").read()
    h = re.sub(r"<title>.*?</title>", "<title>Cheat Sheet · Copilot at Work — KAMCO</title>", s[:s.index("</head>")]) + '<style>.bar-in{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.backlink{font-weight:700;font-size:13px;color:var(--w6);background:var(--w06);border:1px solid var(--w1);border-radius:8px;padding:6px 11px;text-decoration:none}.grid.g4{grid-template-columns:repeat(4,1fr)}@media(max-width:900px){.grid.g4{grid-template-columns:1fr 1fr}}@media(max-width:560px){.grid.g4{grid-template-columns:1fr}}</style></head>\n'

    def item(ac, nm, st, an, df, ex, tl):
        return f'<div class="item" style="--ac:var(--{ac})"><div class="nm">{nm}</div><div class="st">{st}</div><div class="an">{an}</div><div class="df">{df}</div><div class="ex">{ex}</div><div class="tl"><span>Tell</span>{tl}</div></div>'
    parts = [
     ("Part 1", "Ask well", "Three habits that turn a vague answer into a usable one.", "", [
        item("iso", "CTFT", "The prompt recipe", "Like <b>briefing a junior analyst</b>.", "Context, Task, Format, Tone — four parts of every strong prompt.", "“I manage Al-Murjan FO… summarise the 30 Sep export… five bullets in KWD… plain English for a CFO.”", "All four parts are there"),
        item("nist", "Iterate", "Refine, don't restart", "Like <b>a tailor's fitting</b>.", "Treat the first answer as a draft. Improve it in the same chat.", "“Shorter. Breaches first. One decimal place.”", "Short follow-ups, same chat"),
        item("pci", "Source with /", "Point at the file", "Like <b>pointing at the right folder</b>.", "Type / to choose the exact file, email or meeting Copilot must use.", "“Use /amfo-q3-custody-export.xlsx (30 Sep).”", "Every number has a named source")],
      '<span class="iso">CTFT</span> = the brief · <span class="nist">Iterate</span> = the fitting · <span class="pci">/</span> = the source<br><b>Copilot drafts. People decide.</b>'),
     ("Part 2", "One workflow, four apps", "Request → Check → Produce → Reply.", "", [
        item("iso", "Outlook", "Read the request", "Like <b>a chief of staff's one-pager</b>.", "Summarise the thread, then turn it into a checklist: deadline, deliverable, who to copy, what not to do.", "“From this thread, list the final deadline, each deliverable and its format, who to copy, and any request I should not do.”", "The newest message wins"),
        item("nist", "Excel", "Clean, then count", "Like <b>a chef's preparation</b>.", "Remove duplicates, fix text numbers, fill missing prices, clean labels — then build the PivotTable.", "“Highlight duplicate rows based on Holding ID.”", "Row count checked before and after"),
        item("pci", "Word & PowerPoint", "Answer first", "Like <b>a newspaper headline</b>.", "Memo when read alone; deck when presented. Bottom line first. Every slide title is the message.", "“Change every slide title to one sentence that states the main message.”", "Titles alone tell the story")],
      '<span class="iso">Outlook</span> = the ask · <span class="nist">Excel</span> = the numbers · <span class="pci">Word / PowerPoint</span> = the answer<br><b>Feed Copilot numbers you have checked — do not let it re-calculate them.</b>'),
     ("Part 3", "The four checks — before every send", "Like a pilot's checklist: every flight, every send.", " g4", [
        item("iso", "Accuracy", "The numbers", "Like <b>matching receipts</b>.", "Every figure matches your analysis.", "4.5% is not 5.4%.", "Each number traced to the file"),
        item("nist", "Confidentiality", "The people", "Like <b>a sealed envelope</b>.", "Only this client. Only the right recipients.", "Never name another family.", "No other client, right list"),
        item("pci", "Tone", "The voice", "Like <b>answering in the guest's language</b>.", "Fits the reader. No promises of returns.", "Remove “returns will stay strong”.", "No guarantee, no forecast"),
        item("iso", "Completeness", "Everything asked for", "Like <b>a packed suitcase</b>.", "All outputs, attachments, people copied, disclaimer if client-facing.", "Memo and deck both attached.", "Nothing “to follow later”")],
      '<b>You sign the email — not Copilot.</b>'),
    ]
    body = '<body>\n<div class="bar"><div class="bar-in"><a class="backlink" href="index.html" style="margin-right:10px">‹ Back</a><div class="brand"><span class="dot"></span>Cheat Sheet · <b>Copilot at Work</b></div></div></div>\n<main>\n'
    for ph, pt, psub, g, items, sm in parts:
        body += f'<div class="part"><div class="ph">{ph}</div><div class="pt">{pt}</div><div class="psub">{psub}</div><div class="grid{g}">{"".join(items)}</div><div class="sum">{sm}</div></div>\n'
    body += '<div class="part"><div class="note"><span class="ic">⚠</span><div><b>Agents:</b> an agent is only as good as its instructions. Give it one job, clear rules (“always use the newest message”), the right files — and test it before you share it.</div></div></div>\n'
    body += '</main>\n<div class="foot">AI at Work with Microsoft Copilot · CODED × KAMCO Invest — quick reference.</div>\n</body>\n</html>'
    return h + body


if __name__ == "__main__":
    os.makedirs(OUTP, exist_ok=True)
    open(os.path.join(OUTP, "index.html"), "w").write(landing())
    for n in (1, 2):
        open(os.path.join(OUTP, "coded-kamco-day-%d.html" % n), "w").write(day_page(n))
    open(os.path.join(OUTP, "case-files.html"), "w").write(case_files())
    open(os.path.join(OUTP, "before-you-start.html"), "w").write(before_you_start())
    open(os.path.join(OUTP, "cheat-sheet.html"), "w").write(cheat())
    for f in [A["murjan"]["file"], "01-amfo-q3-review-request.eml", "house-view-q4-2026.docx", "my-prompt-library.docx", "abh-q3-custody-export.xlsx", "kgof-q3-fund-pack.xlsx", "ops-q3-settlement-blotter.xlsx", "wafra-logistics-research-pack.xlsx"] + ["capstone-%s-request.eml" % k for k in ("wm", "am", "ops", "rs")]:
        shutil.copy("out/files/" + f, OUTP)
    print(sorted(os.listdir(OUTP)))
