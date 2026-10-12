"""Day 2 deck — MCIM Day 2 (Word, PowerPoint) + MCIM Day 3 (Prompt Library, Agents, Safety)
re-themed for KAMCO, then the KAMCO graded project, MAP post-test, survey and certificates.
Excel, Outlook and Teams are left out (Excel and Outlook were Day 1)."""
import base64, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join(HERE, "templates", "mcim")
SRC = os.path.join(T, "slides")
LAB = "coded-kamco-day-2-lab.html"
LINKS = {"mapPost": "https://portal.joincoded.com/sv/kamco-copilot-map-test-post-day-2",
         "survey": "https://portal.joincoded.com/sv/kamco-copilot-end-of-program-satisfaction-survey"}
ICON = {k: "data:image/png;base64," + base64.b64encode(open(os.path.join(T, k + ".png"), "rb").read()).decode()
        for k in ("word", "powerpoint", "excel", "outlook")}
BG = '<div class="bg-grid"></div><div class="blob b1"></div><div class="blob b2"></div>'
BG1 = '<div class="bg-grid"></div><div class="blob b1"></div>'


def src(name, *reps):
    fn = [f for f in os.listdir(SRC) if f.endswith("-" + name + ".html")]
    assert len(fn) == 1, (name, fn)
    s = open(os.path.join(SRC, fn[0]), encoding="utf-8").read()
    for a, b in reps:
        assert a in s, (name, a[:60])
        s = s.replace(a, b)
    return s


def slide(sid, inner, bg=BG, pad="slide-pad", style=""):
    st = f' style="{style}"' if style else ""
    return f'<div class="slide" id="{sid}">\n{bg}\n<div class="{pad}"{st}>\n{inner}\n</div>\n</div>\n'


def brk(sid, minutes, back, nxt, label=None):
    label = label or f"Break · {minutes} min"
    return slide(sid, f'''<span class="eyebrow b" style="padding-left:0">{label}</span>
<h2 class="term-h b">{"Lunch." if minutes >= 60 else "Break."}</h2>
<div class="mini-timer b" data-min="{minutes}">
<div class="mt-time">{minutes}:00</div>
<div class="mt-bar"><div class="mt-fill"></div></div>
<div class="mt-back">Scheduled: back at {back}</div>
<div class="mt-actions">
<button class="btn" data-d="-5" title="5 minutes less">−5</button>
<button class="btn" data-d="-1" title="1 minute less">−1</button>
<button class="btn primary mt-start">Start</button>
<button class="btn" data-d="1" title="1 minute more">+1</button>
<button class="btn" data-d="5" title="5 minutes more">+5</button>
<button class="btn mt-reset">Reset</button>
</div>
</div>
<p class="brk-next b">Next: <b>{nxt}</b></p>''', pad="slide-pad brk-slide")


def pause(sid, what, nxt):
    return slide(sid, f'''<span class="eyebrow b" style="padding-left:0">Pause</span>
<div class="qmark b">?</div>
<p class="qsub b">Questions on {what}?</p>
<div class="parknote b">🅿️ Quick ones now — then {nxt}</div>''', pad="slide-pad qslide-pad")


def tasks(rows):
    return '<div class="tasks">\n' + "\n".join(
        f'<div class="task b"><span class="tk-id">{i}</span><span class="tk-t">{t}<small>{d}</small></span><span class="tk-m">{m}</span></div>'
        for i, t, d, m in rows) + "\n</div>"


def labcta(eid, label=None):
    return f'<a class="labcta b" href="{LAB}#{eid}" target="_blank" rel="noopener">{label or "Open " + eid + " →"}</a>'


S = []
add = S.append

# ============================== OPENING ==============================
add(slide("s-cover", f'''<span class="eyebrow b" style="padding-left:0">Day 2 · Monday 12 October 2026 · 09:00 – 16:00</span>
<h1 class="cover-h b">Put it to work<br><span class="hl">in Word, PowerPoint and your own agent.</span></h1>
<p class="cover-sub b">Three blocks, then your capstone. Same desk: Al-Murjan, the house view, Faisal's inbox.</p>
<div class="apps-orbit b">
<div class="app-tile"><img class="applogo" src="{ICON['word']}" alt="Word"><span class="an2">Word</span></div>
<div class="app-tile"><img class="applogo" src="{ICON['powerpoint']}" alt="PowerPoint"><span class="an2">PowerPoint</span></div>
<div class="app-tile"><span class="al" style="color:var(--amber)">🤖</span><span class="an2">Agents</span></div>
<div class="app-tile"><span class="al" style="color:var(--rose-lt)">🎯</span><span class="an2">Capstone</span></div>
</div>
<div class="keyhint b">Press → to begin</div>''', style="text-align:center;display:flex;flex-direction:column;align-items:center").replace('<div class="slide" id="s-cover">', '<div class="slide active" id="s-cover">'))

add(slide("s-recap", '''<span class="eyebrow b">Recap · Yesterday</span>
<h2 class="term-h b">Day 1 in four lines.</h2>
<ul class="out-list">
<li class="b"><span class="oc">1</span><span><b>How it works</b> — fluent isn't correct.</span></li>
<li class="b"><span class="oc">2</span><span><b>CTFT</b> — Context, Task, Format, Tone. Plus a Source.</span></li>
<li class="b"><span class="oc">3</span><span><b>Outlook</b> — the newest message wins.</span></li>
<li class="b"><span class="oc">4</span><span><b>Excel</b> — clean first, count second. Then check the mandate.</span></li>
</ul>'''))

add(src("s-hook",
        ('The report is due at 10. The numbers are in Excel, the context is in a thread, the last version is "somewhere in Teams".',
         'The pack is due Tuesday at 3. The numbers are in Excel, the ask is in a thread, the house view is in Word.'),
        ('aria-label="Excel, an email thread and Teams all feeding into you, and you produce the report"',
         'aria-label="Excel, an email thread and the house view all feeding into you, and you produce the client pack"'),
        ('<text class="ill-lbl" x="34" y="162">TEAMS</text>', '<text class="ill-lbl" x="24" y="162">HOUSE VIEW</text>'),
        ('THE REPORT</text>', 'THE PACK</text>'),
        ('Today, Copilot does more of the gluing.', 'Today, Copilot writes, presents and remembers — and you stay the checker.')))

add(slide("s-road", '''<span class="eyebrow b">The Road Today</span>
<h2 class="term-h b">Five stops. <span class="hl">Tap one to jump.</span></h2>
<div class="road">
<div class="road-row go b" data-goto="s-w-story"><span class="rn">01</span><div><div class="rt">Word</div><div class="rd">09:00</div></div></div>
<div class="road-row go b" data-goto="s-p-story"><span class="rn">02</span><div><div class="rt">PowerPoint</div><div class="rd">10:00</div></div></div>
<div class="road-row go b" data-goto="s-g-hook"><span class="rn">03</span><div><div class="rt">Scheduled prompts, libraries + agents</div><div class="rd">11:00</div></div></div>
<div class="road-row go b" data-goto="s-o-reply"><span class="rn">04</span><div><div class="rt">The reply, then your capstone</div><div class="rd">13:00</div></div></div>
<div class="road-row go b" data-goto="s-map-post"><span class="rn">05</span><div><div class="rt">MAP test · survey · certificates</div><div class="rd">15:00</div></div></div>
</div>'''))

# ============================== BLOCK 1 · WORD ==============================
add(slide("s-fmt", """<span class="eyebrow b">Block 1 · First, Pick The Format</span>
<h2 class="demo-h b">Memo or deck? <span class="hl">The reader decides.</span></h2>
<div class="bgcompare b">
<div class="bgcard good"><div class="bgk">Word · report or memo</div><div class="bgp">The reader <b>reads it alone</b>, at a desk, and needs detail, reasons and numbers to check. An Investment Committee pack. A memo to your MD.</div><div class="bgn">One page, bottom line first.</div></div>
<div class="bgcard good"><div class="bgk">PowerPoint · deck</div><div class="bgp">You <b>present it to a room</b> — a client, trustees, a board. People see one idea at a time, and you do the talking.</div><div class="bgn">One slide, one message.</div></div>
</div>
<p class="body-l b">Not sure? Read the request again — <b>who is the reader, and will you be in the room?</b></p>""", bg=BG1))
add(src("s-w-story",
        ('8:40. Your manager wants one page by 10 — from a pile of notes.', '8:40. Faisal wants a one-page memo by 10 — from your meeting notes.')))
add(src("s-w-analogy"))
add(src("s-w-moves", ('⎘ tamra-house-style-letter.docx', '⎘ house-view-q4-2026.docx')))
add(slide("s-w-demo", '''<span class="eyebrow b">Live Demo · Word</span>
<h2 class="demo-h b">One house view → a summary → <span class="hl">a client-ready note.</span></h2>
<div class="demo-card b">
<div class="dc-k">Run in Word · source: house-view-q4-2026.docx · tap to copy</div>
<div class="prompt">Summarise the attached house view for our relationship managers in five bullet points: our view on each asset class, the issuer limit, and what we must never say to clients.</div>
<div class="prompt" style="margin-top:10px">Turn the five points into a short note for a family-office client. Make it 20% shorter and a bit warmer. No jargon.</div>
<div class="prompt" style="margin-top:10px">Check the note against the rules in section 4 of /house-view-q4-2026 and add the standard disclaimer from section 5.</div>
</div>''', bg=BG1))
add(slide("s-w-check", '''<span class="eyebrow b">Quick Check</span>
<h2 class="demo-h b">Copilot's summary says the house view is <span class="hl">Positive on equities</span>. Ship it?</h2>
<div class="qc-card b"><div class="qc-k">Ask the room</div><p>No — equities are <b>Neutral</b>: trim back to the mandate range. <b>Fixed income</b> is the Positive one. Summaries swap rows in a table.</p></div>''', bg=BG1))
add(slide("s-w-lab", f'''<span class="eyebrow b">Hands-On · E2.1 · 20 min</span>
<h2 class="demo-h b">Notes in — <span class="hl">a memo you'd send</span> out.</h2>
{tasks([("1", "Draft", "Your notes from the Al-Murjan prep meeting → a one-page memo to Faisal", "6 min"),
        ("2", "Rewrite", "Shorter. Decisions first. Steer it — don't retype", "4 min"),
        ("3", "Ground", "Type / and add the house view. Match its rules and wording", "5 min"),
        ("4", "Check", "Every number and name against your notes. Fix by hand", "5 min")])}
<p class="done-line b"><b>Done:</b> draft → rewrite → ground → check every fact.</p>
{labcta("E2.1")}'''))
add(pause("s-q-word", "Word", "the break"))
add(brk("s-brk-1", 10, "10:00 AM", "Copilot in PowerPoint"))

# ============================== BLOCK 2 · POWERPOINT ==============================
add(src("s-p-story",
        ('The deck is due at 4. A 12-page report on one screen, a blank slide on the other.',
         'The trustees meet at 11. The house view on one screen, a blank slide on the other.')))
add(src("s-p-analogy"))
add(src("s-p-term"))
add(slide("s-p-demo", '''<span class="eyebrow b">Live Demo · PowerPoint</span>
<h2 class="demo-h b">House view in, <span class="hl">client deck out.</span></h2>
<div class="demo-card b">
<div class="dc-k">Create from file · source: house-view-q4-2026.docx · tap to copy</div>
<div class="prompt">Create a 6-slide client presentation from /house-view-q4-2026: our view in one line, the view on each asset class, the concentration rule, what it means for a balanced portfolio, next steps, and the standard disclaimer on the last slide. Keep every statement traceable to the source. Add speaker notes.</div>
<div class="prompt" style="margin-top:10px">Rewrite every slide title as the message, not the topic. For example: “Equities: back inside the range after a strong Q3” — not “Equities”.</div>
</div>
<p class="body-l b">Save the file to your OneDrive first. Word or PDF both work.</p>''', bg=BG1))
add(src("s-p-check"))
add(slide("s-p-lab", f'''<span class="eyebrow b">Hands-On · E2.2 + E2.3 · 25 min</span>
<h2 class="demo-h b">A document becomes <span class="hl">your deck</span>.</h2>
{tasks([("E2.2", "House view → a 6-slide client deck", "Create from file · add one slide · check two slides against the source", "18 min"),
        ("E2.3", "Titles that say the message", "Stretch: rewrite every title as the “so what” — then cut the deck to three slides", "7 min")])}
<p class="done-line b"><b>Done:</b> a deck, one new slide, two slides checked line by line. Fast? <b>E2.3</b>.</p>
{labcta("E2.2")}'''))
add(pause("s-q-ppt", "PowerPoint", "the break"))
add(brk("s-brk-2", 10, "11:00 AM", "Prompt Library + Agents"))

# ============================== BLOCK 3 · PROMPT LIBRARY + AGENTS ==============================
add(slide("s-g-hook", """<span class="eyebrow b">Block 3 · Prompts That Work For You</span>
<h2 class="demo-h b">You've written about ten prompts in two days. Some you need every week. Some Microsoft already wrote. Some only you know. <span class="hl">Stop retyping them.</span></h2>
<div class="viz-flow">
<div class="vf-step b"><span class="vf-ic"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg></span><span class="vf-t">Schedule</span><span class="vf-d">it runs before you arrive</span></div>
<span class="vf-arrow b">→</span>
<div class="vf-step b"><span class="vf-ic"><svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18"/></svg></span><span class="vf-t">Gallery</span><span class="vf-d">Microsoft's ready-made prompts</span></div>
<span class="vf-arrow b">→</span>
<div class="vf-step b"><span class="vf-ic"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/></svg></span><span class="vf-t">Your library</span><span class="vf-d">the ones that work for you, in Word</span></div>
</div>""", bg=BG1))
add(slide("s-sch-what", """<span class="eyebrow b">1 · Scheduled Prompts</span>
<h2 class="term-h b">Copilot does the Sunday reading <span class="hl">before you arrive.</span></h2>
<div class="bgcompare b">
<div class="bgcard bad"><div class="bgk">Every Sunday, by hand</div><div class="bgp">Open Outlook. Scroll 60 emails. Find the client asks, the deadlines, what Compliance wants.</div><div class="bgn">30 minutes before your first coffee.</div></div>
<div class="bgcard good"><div class="bgk">Scheduled · Sunday 7:30</div><div class="bgp"><span class="sg-ctx">I look after family-office clients.</span> <span class="sg-task">Summarise the emails I received since Thursday from clients and from Compliance.</span> <span class="sg-fmt">A table: who, the ask, the deadline — urgent first.</span> <span class="sg-tone">Short and plain.</span></div><div class="bgn">Waiting in Copilot — and in your inbox — at 7:30.</div></div>
</div>""", bg=BG1))
add(slide("s-sch-how", """<span class="eyebrow b">Scheduled Prompts · How</span>
<h2 class="term-h b">Four steps. <span class="hl">Up to ten schedules.</span></h2>
<ol class="steps-n">
<li class="b"><span><b>Run the prompt once</b> in Copilot Chat — microsoft365.com/chat, Teams or Outlook.<small>Make sure the answer is what you want first.</small></span></li>
<li class="b"><span>Hover over your prompt → <b>Schedule this prompt</b>.</span></li>
<li class="b"><span>Choose <b>when</b> it runs, <b>how many times</b>, and turn on the <b>email notification</b>. Save.</span></li>
<li class="b"><span>Results appear in your chat list on the left.<small>Manage them: <b>…</b> → <b>Scheduled prompts</b> → Run now · Turn off · Delete.</small></span></li>
</ol>
<p class="body-l b">Good to schedule: a <b>repeat</b> question about <b>new</b> information. Not a one-off.</p>""", bg=BG1))
add(src("s-g-what", ('<span class="eyebrow b">Your Prompt Library · In Copilot: “Prompt Gallery”</span>', '<span class="eyebrow b">2 · The Prompt Gallery · Microsoft\'s Library</span>')))
add(src("s-g-adapt",
        ('<span class="sg-ctx">I\'m back after three days off and I manage the wholesale team.</span>',
         '<span class="sg-ctx">I\'m back after three days off and I look after twelve family-office clients.</span>'),
        ('A table: action, who asked, deadline — urgent first.', 'A table: action, client, who asked, deadline — urgent first.')))
add(slide("s-g-word", '''<span class="eyebrow b">3 · Your Own Library · In Word</span>
<h2 class="term-h b">The prompts that work for you — <span class="hl">in one Word file.</span></h2>
<div class="keys">
<div class="key b"><div class="k-ic">📄</div><div><div class="k-t">One file in your OneDrive</div><div class="k-d">My Prompt Library.docx — a table, one row per tested prompt.</div></div></div>
<div class="key b"><div class="k-ic">🧩</div><div><div class="k-t">Name · app · when · the CTFT prompt</div><div class="k-d">[Brackets] where details change. No client names or numbers.</div></div></div>
<div class="key b"><div class="k-ic">↩️</div><div><div class="k-t">Reuse it from Copilot</div><div class="k-d">Type <span class="kbdc">/</span> and pick the file: “From /My Prompt Library, run my mandate check.”</div></div></div>
</div>
<p class="body-l b">The Gallery is Microsoft's library. <b>This one is yours.</b></p>''', bg=BG1))
add(slide("s-g-lab", f'''<span class="eyebrow b">Hands-On · 20 min</span>
<h2 class="demo-h b">Schedule one. Borrow one. <span class="hl">Keep your own.</span></h2>
{tasks([("E2.4", "Schedule a prompt", "A weekly prompt that runs on Sunday morning — run it once, schedule it, test with Run now", "5 min"),
        ("E2.5", "Library hunt", "Prompt Gallery: find three for your role, adapt one with CTFT, run it, save it", "8 min"),
        ("E2.6", "Your prompt library in Word", "Download the template, add your three best prompts, reuse one with /", "7 min")])}
<p class="done-line b"><b>Done:</b> one scheduled prompt · one Gallery prompt adapted and saved · a Word library with three of your own.</p>
{labcta("E2.4")}''', bg=BG1))
add(src("s-a-hook",
        ('Block 2 · Agent Builder', 'Block 3 · Agents'),
        ('Every time, you paste the same context: who you are, which file, what format.',
         'Every Sunday, Faisal\'s team reads forty client requests: the client, the ask, the deadline, the risks. Same steps every week.')))
add(src("s-a-what"))
add(slide("s-a-builtin", '''<span class="eyebrow b">Agents Built By Microsoft</span>
<h2 class="term-h b">Some agents are <span class="hl">ready to use.</span></h2>
<div class="sys3">
<div class="sys s1 b"><div class="sn">Analyst</div><h3>Data → insight</h3><p>Turns raw data into findings and charts — and shows its working.</p></div>
<div class="sys s2 b"><div class="sn">Researcher</div><h3>Deep research</h3><p>Gathers and summarises from your work files and the web, with sources.</p></div>
<div class="sys s3 b"><div class="sn">Prompt Coach</div><h3>Better prompts</h3><p>Shows you how to structure a prompt. Find it under <b>All agents</b>.</p></div>
</div>
<p class="body-l b">Copilot app → <b>Agents</b> in the left panel. Not there? Your IT team may not have switched it on.</p>''', bg=BG1))
add(slide("s-a-lab1", f'''<span class="eyebrow b">Hands-On · E2.7 · 10 min</span>
<h2 class="demo-h b">Use a built-in agent — <span class="hl">and check its numbers.</span></h2>
{tasks([("1", "Analyst", "Give it the Al-Murjan export. Ask for allocation against the mandate and the issuer check. Compare with your Day 1 answers.", "6 min"),
        ("2", "Prompt Coach", "Paste one prompt from your Word library. Take one suggestion — then save the better version.", "4 min")])}
<p class="done-line b"><b>Done:</b> one agent answer checked against numbers you trust · one prompt improved.</p>
{labcta("E2.7")}''', bg=BG1))
add(src("s-a-how", ('Five steps to <span class="hl">your first agent.</span>', 'Now build <span class="hl">your own.</span> Five steps.')))
add(slide("s-a-instr", '''<span class="eyebrow b">Instructions = CTFT</span>
<h2 class="demo-h b">Instructions are a prompt <span class="hl">that never goes away.</span></h2>
<div class="bgcompare b">
<div class="bgcard bad"><div class="bgk">Weak</div><div class="bgp">Read client requests.</div><div class="bgn">It guesses everything.</div></div>
<div class="bgcard good"><div class="bgk">Strong — CTFT</div><div class="bgp"><span class="sg-ctx">You help KAMCO wealth management staff read client requests.</span> <span class="sg-task">For any email or thread: the client, each requested output and its format, the final deadline — always the newest message — and who to copy. Flag anything that breaks section 4 of the house view.</span> <span class="sg-fmt">Answer in a table.</span> <span class="sg-tone">Plain and short. Unclear? Say so — do not guess.</span></div><div class="bgn">Now it knows its job.</div></div>
</div>''', bg=BG1))
add(src("s-a-know"))
add(slide("s-a-lab", f'''<span class="eyebrow b">Hands-On · E2.8 · 20 min</span>
<h2 class="demo-h b">Build an agent for <span class="hl">your field.</span> Then try to break it.</h2>
{tasks([("WM", "Request Triage Assistant", "Wealth Management · reads client requests against the house view", ""),
        ("AM · RS", "Fund Rules · Research Rules", "Asset Management · Investment Research", ""),
        ("OPS · FIN", "Operations Procedures · Expense Policy", "Operations · Finance", ""),
        ("HR · LC", "HR Policy Helper · Compliance Checker", "Human Resources · Legal &amp; Compliance", "")])}
<p class="done-line b"><b>Build</b> 6 min · <b>test six ways</b> 10 min · <b>fix</b> 4 min. Pick your field in the lab — each has its own knowledge file and tests.</p>
{labcta("E2.8")}''', bg=BG1))
add(src("s-a-check"))
add(pause("s-q-agent", "agents", "lunch"))
add(brk("s-brk-3", 60, "1:00 PM", "The reply in Outlook — then your capstone", label="Lunch · 60 min"))

# ============================== GRADED PROJECT ==============================
add(slide("s-o-reply", """<span class="eyebrow b">After Lunch · The Reply · Outlook</span>
<h2 class="demo-h b">The reply <span class="hl">matches the request.</span></h2>
<div class="demo-card b">
<div class="dc-k">Live demo · Copilot in Outlook · reply to Faisal's thread · tap to copy</div>
<div class="prompt">Draft my reply to Faisal. Confirm the 5-slide deck and the one-page memo are attached, give the bottom line in one sentence, and say I copied Noura in Compliance. Match the tone of his email — short and direct. Under 100 words.</div>
<div class="prompt" style="margin-top:10px">Add one polite line declining Khalid's request for the Al-Rumaithiya report, because it is another client's data. Offer a blank sample of our format instead.</div>
</div>
<p class="body-l b">Steer, don't retype: <b>“shorter”</b> → <b>“a little warmer”</b>. Then run Coaching before you send.</p>""", bg=BG1))
add(slide("s-o-coach", """<span class="eyebrow b">Coaching By Copilot</span>
<h2 class="term-h b">A second pair of eyes — <span class="hl">before you hit Send.</span></h2>
<div class="keys">
<div class="key b"><div class="k-ic">🎯</div><div><div class="k-t">Tone</div><div class="k-d">Too blunt, too soft, too long for an MD?</div></div></div>
<div class="key b"><div class="k-ic">👤</div><div><div class="k-t">Reader sentiment</div><div class="k-d">How will Faisal — or the client — feel reading it?</div></div></div>
<div class="key b"><div class="k-ic">🔎</div><div><div class="k-t">Clarity</div><div class="k-d">Is the ask, the answer and the next step obvious?</div></div></div>
</div>
<p class="body-l b">In Outlook: write the draft → select <b>Copilot</b> → <b>Coaching by Copilot</b>. You decide which suggestions to keep.</p>""", bg=BG1))
add(slide("s-r-checklist", """<span class="eyebrow b">Checking The Work · Before You Hit Send</span>
<h2 class="term-h b">Four checks, every time<span class="hl">.</span></h2>
<div class="checks">
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">Accuracy</div><div class="c-d">Every number traced back to Excel. Every claim to its source.</div></div></div>
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">Confidentiality</div><div class="c-d">No other client's data. Compliance copied if it goes to a client.</div></div></div>
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">Tone</div><div class="c-d">Right for the reader. No promises of returns. Coaching by Copilot.</div></div></div>
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">Completeness</div><div class="c-d">Every ask in the newest email answered. Both files attached.</div></div></div>
</div>
<p class="body-l b">You sign it. <b>You own it.</b></p>"""))
add(slide("s-c-brief", """<span class="eyebrow b">Capstone · Graded · 13:10 – 14:50</span>
<h2 class="term-h b">Your field. One request. <span class="hl">Start to finish — alone.</span></h2>
<div class="road">
<div class="road-row b"><span class="rn">01</span><div><div class="rt">Summarise the request · Outlook</div><div class="rd">Final deadline, two files, who they're for — and the ask you must decline. 10 min</div></div></div>
<div class="road-row b"><span class="rn">02</span><div><div class="rt">Clean the data · Excel</div><div class="rd">Duplicates, text numbers, messy labels. Row count before and after. 15 min</div></div></div>
<div class="road-row b"><span class="rn">03</span><div><div class="rt">Analyse · Excel</div><div class="rd">Answer every question in the email — show the formula. 18 min</div></div></div>
<div class="road-row b"><span class="rn">04</span><div><div class="rt">Chart it · Excel</div><div class="rd">Titles that say the message. 8 min</div></div></div>
<div class="road-row b"><span class="rn">05</span><div><div class="rt">Executive brief · Word</div><div class="rd">One page, bottom line first, grounded in the house view. 18 min</div></div></div>
<div class="road-row b"><span class="rn">06</span><div><div class="rt">The deck · PowerPoint</div><div class="rd">Six slides created from your brief. 18 min</div></div></div>
<div class="road-row b"><span class="rn">07</span><div><div class="rt">Check and reply · Outlook</div><div class="rd">Four checks. Email your reply with both files to aya@joincoded.com by 2:50 pm. End with “What I corrected: …” 13 min</div></div></div>
</div>"""))
add(slide("s-c-fields", f"""<span class="eyebrow b">Capstone · Pick Your Field</span>
<h2 class="term-h b">Seven desks. <span class="hl">Pick the one closest to your job.</span></h2>
{tasks([("WM", "Wealth Management", "Al-Bayan Holding Q3 review · brief for the Investment Committee, client deck", ""),
        ("AM", "Asset Management", "Gulf Opportunities Fund Q3 · fund vs benchmark, fund rules, flows", ""),
        ("RS", "Investment Research", "Wafra Logistics initiation · peer valuation and a view", ""),
        ("OPS", "Operations", "Q3 settlement review · on-time rate, fails, escalations", ""),
        ("FIN", "Finance", "Q3 budget vs actual · variances and who must explain", ""),
        ("HR", "Human Resources", "Q3 people review · attrition, exit reasons, training, engagement", ""),
        ("LC", "Legal &amp; Compliance", "Q3 complaints review · on-time standards, overdue cases", "")])}
<p class="body-l b">Everything is in the lab: the email thread, the workbook, the house view. <b>Lab → E2.9 → pick your field.</b></p>""", bg=BG1))
add(slide("s-c-rubric", """<span class="eyebrow b">How It's Scored · /100 · Pass / Does not pass</span>
<h2 class="term-h b">Five criteria. <span class="hl">Help from Copilot is the point.</span></h2>
<div class="checks">
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">30 · Workflow completeness</div><div class="c-d">Read the email, analysed the data, produced the brief and the deck, sent the reply — all seven steps, by 2:50 pm.</div></div></div>
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">25 · Data analysis accuracy</div><div class="c-d">Copilot's output reviewed and corrected. No major data errors in the final files.</div></div></div>
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">20 · Deliverable quality</div><div class="c-d">Brief, deck and charts are clear, professional and answer the request.</div></div></div>
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">15 · AI review &amp; judgement</div><div class="c-d">Accuracy, confidentiality, tone, completeness — your “What I corrected” line.</div></div></div>
<div class="check-row b"><div class="cbox"></div><div><div class="c-t">10 · Prompt quality</div><div class="c-d">Paste your three best prompts at the end of your reply — specific, with context, task, format and tone.</div></div></div>
</div>
<p class="body-l b">Work alone. Submit by <b>2:50 pm</b>: email your final reply with <b>both files attached</b> to <b>aya@joincoded.com</b>.</p>"""))
add(slide("s-c-go", f'''<span class="eyebrow b">Capstone · 100 minutes</span>
<h2 class="term-h b">Build it<span class="hl">.</span></h2>
<div class="maptest-row b">
<div class="mini-timer" data-min="100" style="margin-top:0;flex:1;min-width:280px">
<div class="mt-time">100:00</div>
<div class="mt-bar"><div class="mt-fill"></div></div>
<div class="mt-actions">
<button class="btn primary mt-start">Start 100:00</button>
<button class="btn mt-plus">+2 min</button>
<button class="btn mt-reset">Reset</button>
</div>
</div>
</div>
<p class="done-line b"><b>Submit to aya@joincoded.com.</b> <b>Pace:</b> by 13:55 your numbers are done · by 14:35 the brief and the deck · by 14:50 the reply is sent. <b>Finished early?</b> Do the Stretch and Boss in your field.</p>
{labcta("E2.9", "Open the capstone →")}'''))
add(slide("s-present", """<span class="eyebrow b">14:50 · Present Your Workflow · 2 Minutes Each</span>
<h2 class="term-h b">Show your partner <span class="hl">the whole journey.</span></h2>
<div class="maptest-row b">
<div class="mini-timer" data-min="2" style="margin-top:0;flex:1;min-width:280px">
<div class="mt-time">2:00</div>
<div class="mt-bar"><div class="mt-fill"></div></div>
<div class="mt-actions">
<button class="btn primary mt-start">Start 2:00</button>
<button class="btn mt-reset">Reset</button>
</div>
</div>
</div>
<ol class="steps-n">
<li class="b"><span><b>The request</b> — your field, the reader, the real deadline.</span></li>
<li class="b"><span><b>One number and one chart</b> — the finding that matters most.</span></li>
<li class="b"><span><b>What I corrected</b> — the one thing Copilot got wrong.</span></li>
</ol>
<p class="done-line b">Swap at 2:00. Then the MAP test.</p>"""))


# ============================== MAP · SURVEY · CERTIFICATES · CLOSE ==============================
add(src("s-map-post",
        ('Post-Workshop · 11:30', 'Post-Workshop · 15:00'),
        ('Same map as Tuesday. 30 minutes.', 'Same test as Sunday morning. 30 minutes. See how far you travelled.')))
add(src("s-survey",
        ('Certificates + Survey · 2:00', 'Survey + Certificates · 15:30'),
        ('Ten minutes. Certificates come to you while you fill it in.', 'Five minutes. Then certificates, by name.'),
        ('Satisfaction survey · 10 minutes', 'Satisfaction survey · 5 minutes'),
        ("It shapes the next group's workshop.", 'It shapes Program 3 — and the next group.')))
add(slide("s-journey", '''<span class="eyebrow b">Two Days</span>
<h2 class="term-h b">From a request in your inbox — <span class="hl">to a reply you can stand behind.</span></h2>
<div class="road">
<div class="road-row b"><span class="rn">SUN</span><div><div class="rt">You found the real ask and checked the numbers</div><div class="rd">Outlook and Excel on the Al-Murjan request.</div></div></div>
<div class="road-row b"><span class="rn">MON</span><div><div class="rt">You wrote, presented and automated — safely</div><div class="rd">Word, PowerPoint, prompt libraries, agents — and your capstone.</div></div></div>
<div class="road-row b"><span class="rn">NEXT</span><div><div class="rt">AI in Investments · Program 3</div><div class="rd">Evaluation results follow from KAMCO and CODED.</div></div></div>
</div>
<p class="body-l b">Before you go: save your best prompts in <b>Your prompts</b> in Copilot.</p>''', bg=BG1))
add(slide("s-close", f'''<span class="eyebrow b" style="padding-left:0">Close</span>
<h2 class="cover-h b" style="font-size:clamp(32px,5.5vw,62px)">Copilot works for you now<span class="hl">.</span></h2>
<p class="cover-sub b">Keep the cheat sheet open. Keep the checker's eye. Thank you.</p>
<div class="apps-orbit b">
<div class="app-tile"><img class="applogo" src="{ICON['outlook']}" alt=""><span class="an2">Outlook</span></div>
<div class="app-tile"><img class="applogo" src="{ICON['excel']}" alt=""><span class="an2">Excel</span></div>
<div class="app-tile"><img class="applogo" src="{ICON['word']}" alt=""><span class="an2">Word</span></div>
<div class="app-tile"><img class="applogo" src="{ICON['powerpoint']}" alt=""><span class="an2">PowerPoint</span></div>
</div>''', style="text-align:center;display:flex;flex-direction:column;align-items:center"))


def build(out_path):
    shell = open(os.path.join(T, "deck-shell.html"), encoding="utf-8").read()
    i = shell.index("<!-- ===================== DAY 3")
    j = shell.index('\n<div class="deck-nav">')
    html = shell[:i] + "\n".join(S) + shell[j:]
    html = re.sub(r'<script src="site-config\.js"></script>',
                  '<script>window.SITE={links:%s};</script>' % __import__("json").dumps(LINKS), html, count=1)
    html = html.replace('href="coded-copilot-day-3.html" title="Back to the Day 3 page"', 'href="coded-kamco-day-2.html" title="Back to the Day 2 page"')
    html = html.replace("<span>Day 3</span></a>", "<span>Day 2</span></a>", 1)
    html = re.sub(r"<title>.*?</title>", "<title>Day 2 Slides — AI at Work with Microsoft Copilot · CODED × KAMCO</title>", html, count=1)
    html = html.replace("Mastering Copilot in Microsoft 365", "AI at Work with Microsoft Copilot")
    qr = open(os.path.join(T, "qrcode.min.js"), encoding="utf-8").read()
    html = html.replace('<script src="qrcode.min.js"></script>', "<script>" + qr + "</script>", 1)
    assert "<script src=" not in html
    open(out_path, "w", encoding="utf-8").write(html)
    return len(S)


if __name__ == "__main__":
    print("day 2 deck:", build(os.path.join(HERE, "out/site/coded-kamco-day-2-deck.html")), "slides")
