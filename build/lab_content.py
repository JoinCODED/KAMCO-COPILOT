import json, html as H
from emails import MURJAN_THREAD, WAHA_THREAD, TRIAGE, TRIAGE_I, TRIAGE_OPTS, thread_text

A = json.load(open("out/answers.json"))
M = A["murjan"]; W = A["waha"]


def kwd(x):
    return "KWD {:,.0f}".format(x)


def mail_block(t):
    return H.escape(thread_text(t))


def ch(id, no, cat, pts, diff, title, scn, obj, wild, engine, data, sol=None, walk=None, extra=None):
    data = dict(data, resetId=id)
    c = dict(id=id, no=no, cat=cat, pts=pts, diff=diff, title=title, scn=scn, obj=obj, wild=wild, engine=engine, data=data)
    if sol: c["sol"] = sol
    if walk: c["walk"] = walk
    if extra: c["extra"] = extra
    return c


def sel(label, opts, answer, why, hint=None):
    return dict(kind="select", label=label, opts=opts, answer=answer, why=why, hint=hint)


def num(label, answer, tol, unit, why, hint=None, ph=None):
    return dict(kind="num", label=label, answer=answer, tol=tol, unit=unit, why=why, hint=hint, ph=ph)


FILES = 'Files: <a href="case-files.html" target="_blank">the case file page</a> (thread + Excel export).'
SAFE_OPTS = [dict(k="ok", label="Fine in work Copilot"), dict(k="strip", label="Fine after removing personal data"), dict(k="never", label="Never")]
CTFT_OPTS = [dict(k="c", label="Context"), dict(k="t", label="Task"), dict(k="f", label="Format"), dict(k="o", label="Tone")]


def murjan_triage():
    return [dict(frm=m["frm"], em=m["em"], subj=m["subj"], body=m["body"], key=m["key"]) for m in TRIAGE]


# ======================= DAY 1 · TRAINEE (Al-Murjan) =======================
def mvp(a):
    return a["alloc_pct"]


D1T = [
 ch("d1-safe", 1, "AI", 100, "EASY", "Safe or Not?",
    "Before you open any client file, decide what may go into Copilot — and where.",
    "Put each item in the right bucket. <b>Share only what the task needs, and only with your KAMCO work account.</b>",
    "Samsung (2023): staff pasted confidential code and notes into a public chatbot three times in twenty days. The company then banned public AI tools.",
    "assign", dict(flag="KAMCO{share_only_what_the_task_needs}", opts=SAFE_OPTS,
     intro="Your KAMCO work account gives you enterprise data protection. That does not mean everything belongs in a prompt.",
     items=[dict(html="The 30 Sep custody export for Al-Murjan Family Office — your client — to analyse it.", key="ok", why="Your client, your task, your work tenant."),
            dict(html="A client complaint email with the client's mobile number and civil ID — you want a summary of the complaint.", key="strip", why="The summary does not need the ID or phone number. Replace them with placeholders first."),
            dict(html="The Q4 2026 House View from the research portal.", key="ok", why="Internal document, inside KAMCO's boundary, needed for the task."),
            dict(html="Your KAMCO password, so Copilot can log in to a portal for you.", key="never", why="Never share passwords with any tool or person."),
            dict(html="Al-Murjan's holdings pasted into a free public chatbot on your personal phone.", key="never", why="No enterprise data protection. Client data never goes there.")]),
    extra='In Copilot Chat (work account), ask: “What should staff at an investment firm never paste into an AI tool? Give five examples.” Compare with your answers. Did it miss anything — or add something you disagree with?',
    sol=dict(steps=['<span class="verdict v-pick">Fine</span> the custody export and the house view — your client, your task, work account.',
                    '<span class="verdict v-pick">After removing personal data</span> the complaint email — the summary does not need the civil ID or phone number.',
                    '<span class="verdict v-phish">Never</span> your password, and client data in a public chatbot.'],
             point="Even inside a safe tool, share only what the task needs.")),
 ch("d1-ctft", 2, "PRM", 100, "EASY", "Build the Brief",
    "Faisal's colleague wrote a strong prompt for the Al-Murjan pack. Pull it apart to see why it works.",
    "Label each part of the prompt as <b>Context, Task, Format or Tone</b>.",
    "Morgan Stanley's adviser assistant (2023) worked because questions were specific and grounded in the firm's own research.",
    "assign", dict(flag="KAMCO{context_task_format_tone}", opts=CTFT_OPTS,
     intro="One prompt, five pieces. Which ingredient is each piece?",
     items=[dict(html="“I am the relationship manager for Al-Murjan Family Office. The CFO meets us on Wednesday 14 Oct.”", key="c", why="The situation: who you are and why."),
            dict(html="“Using /amfo-q3-custody-export.xlsx, calculate the value at 30 Sep and the Q3 change.”", key="t", why="The job to do, with a named source."),
            dict(html="“Show the result as a table with two columns: measure and value in KWD.”", key="f", why="How the output must look."),
            dict(html="“Write it in plain English for a family CFO, no jargon.”", key="o", why="The voice."),
            dict(html="“Flag any asset class outside the mandate range.”", key="t", why="Another part of the task.")]),
    extra="Rewrite the same prompt for a different reader: the Al-Murjan summary for the family's 25-year-old son who is new to investing. Change only the <b>Context</b> and <b>Tone</b>, run both in Copilot Chat and compare.",
    sol=dict(steps=["Context: who you are + the CFO meeting.", "Task: calculate value and Q3 change; flag mandate breaches (two task pieces).", "Format: a two-column table in KWD.", "Tone: plain English for a family CFO."],
             point="A prompt can have more than one task line — but every strong prompt has all four parts.")),
 ch("d1-summary", 3, "OUT", 150, "MODERATE", "Summarise the Thread",
    "Faisal's thread has three messages, and the instructions changed twice. Copilot's summary looks tidy — but summaries can mix old and new instructions.",
    "In Outlook, open the Al-Murjan thread and click <b>Summarise</b>. Then check this Copilot-style summary against the thread and click the <b>three</b> points that are wrong.",
    "Microsoft's Work Trend Index (2023) found people spend about 57% of their time communicating. A fast summary only saves time if it is right.",
    "bec", dict(flag="KAMCO{check_the_summary_against_the_thread}", need=["date", "src", "conf"], btn="Submit the 3 wrong points →", hbtn="▾ Show thread details",
     wrongMsg="Not quite. Check each point against the newest message — dates, the source file, and what you are allowed to send.",
     intro="Your own Summarise result may look different. That is the point: compare every line with the thread before you act on it.",
     head='<div class="ph">COPILOT · SUMMARY</div><div class="pf">RE: FW: Al-Murjan FO - Q3 review pack · 3 messages</div>',
     headers="From: Faisal Al-Mutairi, Khalid Al-Murjan · 8–11 Oct 2026",
     body=('<div class="pbody"><p>• <span class="tl" data-k="ok1">Faisal needs a Q3 review pack for Al-Murjan Family Office: a 5-slide client deck and a one-page memo for him.</span></p>'
           '<p>• <span class="tl" data-k="date">The pack is due on Wednesday 14 Oct.</span></p>'
           '<p>• <span class="tl" data-k="ok2">The client meeting has moved to Wednesday 14 Oct at 11:00.</span></p>'
           '<p>• <span class="tl" data-k="src">Use the June factsheet for the figures.</span></p>'
           '<p>• <span class="tl" data-k="ok3">Khalid asks how much sits with Al-Noor Bank and whether equities are inside the mandate.</span></p>'
           '<p>• <span class="tl" data-k="conf">Action: send Khalid the Al-Rumaithiya family report as a format example.</span></p>'
           '<p>• <span class="tl" data-k="ok4">Copy Noura in Compliance before anything goes to the client.</span></p></div>')),
    extra="In Outlook, ask Copilot: “Draft a polite reply to Khalid. Decline to share another family's report and offer a blank sample of our format instead.” Then run <b>Coaching by Copilot</b> on the draft.",
    sol=dict(steps=["Run <b>Summarise</b> on the thread in Outlook and read the newest message yourself.",
                    '<span class="verdict v-phish">Wrong</span> “due Wednesday 14 Oct” — Faisal moved it to <b>Tuesday 13 Oct, 3:00 pm</b>.',
                    '<span class="verdict v-phish">Wrong</span> “use the June factsheet” — Faisal said the opposite: use the <b>30 Sep custody export</b>.',
                    '<span class="verdict v-phish">Wrong</span> “send the Al-Rumaithiya report” — another client\'s data never leaves. Decline politely.',
                    '<span class="verdict v-legit">Correct</span> the deliverables, the new meeting time, Khalid\'s two questions, and copying Noura.'],
             point="A summary is a starting point. Check it against the newest message before you act.")),
 ch("d1-request", 4, "OUT", 200, "MODERATE", "Read the Request",
    "Faisal's thread has three messages. The instructions changed twice.",
    "Use Copilot in Outlook (Summarise + a prompt) on the Al-Murjan thread — then answer. <b>The newest message wins.</b>",
    "The most common reason a pack is late: someone worked from the first email in the thread.",
    "answer", dict(flag="KAMCO{the_newest_message_wins}", mail=mail_block(MURJAN_THREAD),
     intro="The full thread is below if it is not in your inbox. Prompt idea: “From this thread, list the final deadline, each deliverable and its format, who to copy, and any request I should not do.”",
     fields=[sel("What is the final deadline for your pack?", ["Wed 14 Oct", "Tue 13 Oct, 3:00 pm", "Thu 15 Oct"], 1, "Faisal moved it in the newest message."),
             sel("When is the client meeting?", ["Thu 15 Oct", "Wed 14 Oct, 11:00", "Tue 13 Oct, 3:00 pm"], 1, "Khalid moved the meeting to Wednesday 11:00."),
             sel("What must you deliver?", ["A one-page memo only", "A 5-slide client deck and a one-page memo for Faisal", "A 4-slide deck"], 1, "Deck for the client, memo for Faisal."),
             sel("Who must be copied before anything goes to the client?", ["Khalid Al-Murjan", "Noura in Compliance", "Nobody"], 1, "Faisal asked you to copy Noura in Compliance."),
             sel("Which request must you decline?", ["Faisal's request for a memo", "Khalid's request for the Al-Rumaithiya family's report", "Khalid's question about Al-Noor Bank"], 1, "Another client's report never leaves. Offer a blank sample of the format instead.")]),
    extra='Ask Copilot to turn the thread into a timed to-do list for Sunday and Monday, working back from the Tuesday 3:00 pm deadline. Is the plan realistic?',
    sol=dict(steps=["Run <b>Summarise</b> on the thread, then the checklist prompt.", "Deadline: <b>Tue 13 Oct, 3:00 pm</b> (newest message). Meeting: <b>Wed 14 Oct, 11:00</b>.", "Deliverables: <b>5-slide client deck + one-page memo</b>. Copy: <b>Noura in Compliance</b>.",
                    "Decline: <b>the Al-Rumaithiya family report</b> — confidential to another client."], point="The newest message wins — and some requests must be declined, politely.")),
 ch("d1-clean", 5, "XLS", 200, "MODERATE", "Clean the Export",
    "The Al-Murjan custody export has duplicates, numbers stored as text, missing prices and messy labels.",
    "Clean it with Copilot in Excel (the five prompts from the deck). Then enter what you found.",
    "Reinhart & Rogoff (2013): one spreadsheet range left out five countries and changed a global debate.",
    "answer", dict(flag="KAMCO{clean_before_you_count}",
     intro="Delete the title rows, press Ctrl+T, then clean. " + FILES,
     fields=[num("How many data rows are in the raw export (below the headers)?", M["raw_rows"], 0, "rows", "Right — before cleaning.", "Count the rows below the header row."),
             num("How many duplicate rows did you remove?", M["duplicates"], 0, "rows", "Right — four holdings appeared twice.", "Highlight duplicates by Holding ID."),
             num("How many holdings are left after cleaning?", M["holdings"], 0, "holdings", "Right — 22 unique holdings.", "Raw rows minus duplicates."),
             sel("Which two tickers had a missing 30 Sep price?", ["ATLS and GTB", "NWH and GHR", "CVC and SPF"], 1, "Right — filled from the Price_List sheet.", "Filter Price 30-Sep-2026 for blanks.")]),
    extra='Ask Copilot in Excel: “Which columns still have inconsistent values?” Then fix the <b>Price Date</b> column so every value is a real date.',
    sol=dict(steps=[f"Raw export: <b>{M['raw_rows']}</b> rows.", f"Duplicates by Holding ID: <b>{M['duplicates']}</b> (Atlas Tech, Gulf Trade Bank, US Treasury 2030, Failaka Foods).", f"After removal: <b>{M['holdings']}</b> holdings.", "Missing prices: <b>NWH</b> and <b>GHR</b> — filled from Price_List."],
             point="Check the row count before and after every cleaning step.")),
 ch("d1-value", 6, "XLS", 250, "HARD", "Value and Mandate",
    "Faisal's first two questions: what is the portfolio worth, and are we inside the mandate?",
    "Add Market Value KWD, then a PivotTable by asset class with % of total. Compare with the Mandate sheet.",
    "JPMorgan's “London Whale” (2012): a spreadsheet error in a risk model helped hide the size of the risk.",
    "answer", dict(flag="KAMCO{check_the_mandate}",
     intro="Remember: USD × 0.3065 = KWD. Q3 change = value at 30 Sep minus value at 30 Jun (quantities did not change). " + FILES,
     fields=[num("Total portfolio value at 30 Sep (KWD, no decimals)", M["total_sep"], 1500, "KWD", "Right.", "Did you remove the duplicates and fill the two missing prices?", "e.g. 4,500,000"),
             num("Q3 change in % (one or two decimals)", M["q3_return_pct"], 0.05, "%", "Right.", "Total at 30 Sep ÷ total at 30 Jun − 1."),
             num("Equity weight at 30 Sep (%)", M["alloc_pct"]["Equity"], 0.15, "%", "Right.", "Equity value ÷ total value. Did you clean the asset class labels?"),
             sel("Which asset class is outside its mandate range?", ["None", "Equity", "Fixed Income", "Real Estate", "Cash"], 1, f"Equity at {M['alloc_pct']['Equity']}% is above the 55% maximum.")]),
    extra='Add a column that shows how far each asset class is from its mandate minimum or maximum, in percentage points. Then ask Copilot to chart allocation against target.',
    sol=dict(steps=[f"Total value at 30 Sep: <b>{kwd(M['total_sep'])}</b> (with duplicates it would be {kwd(M['wrong_if_dups_kept'])} — wrong).",
                    f"Q3 change: <b>{kwd(M['q3_change'])}</b> = <b>{M['q3_return_pct']}%</b>.",
                    "Allocation: " + ", ".join(f"{a} <b>{v}%</b>" for a, v in M["alloc_pct"].items()) + ".", "Breach: <b>Equity</b> (max 55%)."],
             point="A total is only right if the rows under it are clean.")),
 ch("d1-issuer", 7, "XLS", 250, "HARD", "Issuers and Movers",
    "Khalid asked how much of the portfolio sits with Al-Noor Bank. Faisal wants the top and bottom contributors.",
    "Sum value by Issuer (shares and bonds together, no cash). Then add Q3 Change KWD per holding.",
    "Issuer limits exist because one name can hide in two asset classes: a bank's shares and its sukuk.",
    "answer", dict(flag="KAMCO{the_whole_issuer_counts}",
     intro="Issuer exposure = all holdings from the same issuer (equity + fixed income) ÷ total portfolio value. " + FILES,
     fields=[sel("Which issuer is the largest exposure?", ["Atlas Tech Corp", "Al-Noor Bank", "Gulf Sovereign", "US Treasury"], 1, "Shares plus sukuk together."),
             num("Its weight (% of total portfolio)", M["issuer_top"][0][1], 0.1, "%", "Right — above the 10% limit.", "Add the Al-Noor Bank shares AND the Al-Noor Bank Sukuk 2029."),
             sel("Top contributor in Q3 (KWD)", ["Atlas Tech Corp", "Harbor Semiconductors", "Al-Noor Bank", "World Equity Tracker ETF"], 2, f"Al-Noor Bank shares: +{M['top3'][0][1]:,} KWD."),
             sel("Bottom contributor in Q3 (KWD)", ["Northwind Health", "Gulf Horizon REIT", "Sadaf Logistics", "Gulf Trade Bank"], 2, f"Sadaf Logistics: {M['bottom3'][0][1]:,} KWD.")]),
    extra='Ask Copilot: “How much of Al-Noor Bank (in KWD) would we need to sell to bring it back to 10% of the portfolio?” Check its maths by hand — you should get about KWD 104,000.',
    sol=dict(steps=[f"Al-Noor Bank shares + sukuk = <b>{M['issuer_top'][0][1]}%</b> → above the 10% limit.",
                    "Top 3: " + ", ".join(f"{n} (+{v:,})" for n, v in M["top3"]) + ".", "Bottom 3: " + ", ".join(f"{n} ({v:,})" for n, v in M["bottom3"]) + "."],
             point="The issuer limit counts the whole issuer — shares and bonds together.")),
]

# ======================= DAY 1 · INSTRUCTOR (Al-Waha) =======================
D1I = [
 ch("i1-safe", 1, "AI", 100, "EASY", "Safe or Not?", "Show the room how to decide what goes into a prompt.", "Sort each item into a bucket — out loud.",
    "Samsung (2023): three leaks in twenty days, then a ban on public AI tools.",
    "assign", dict(flag="KAMCO{work_account_only}", opts=SAFE_OPTS, intro="Different examples from the trainee lab — same idea.",
     items=[dict(html="The Al-Waha 30 Sep custody export, to calculate allocation.", key="ok", why="Your client, your task."),
            dict(html="A scanned passport copy from a client's onboarding file, to “read the name”.", key="never", why="Not needed for the task. Never paste ID documents."),
            dict(html="Meeting notes that mention a client's health problem — you want the action points.", key="strip", why="Remove the personal detail; keep the actions."),
            dict(html="A public news article about Gulf banks.", key="ok", why="Public information."),
            dict(html="The Al-Waha holdings, in a public chatbot, because Copilot is slow today.", key="never", why="Slow is not a reason. Client data stays in work Copilot.")]),
    walk=dict(say="“Copilot with your work account is safe. That does not mean everything belongs in it.”", do=["Read each item aloud; ask the room to call the bucket.", "Stop on the health-notes item: what would you remove?", "Submit → flag."], point="Work account only — and only what the task needs.")),
 ch("i1-ctft", 2, "PRM", 100, "EASY", "Build the Brief", "Pull apart a strong prompt for the Al-Waha memo.", "Label each piece C, T, F or T.",
    "Good prompts are briefs.", "assign", dict(flag="KAMCO{brief_it_like_a_colleague}", opts=CTFT_OPTS, intro="One prompt, five pieces.",
     items=[dict(html="“I advise the Al-Waha family. They are worried about property.”", key="c", why="Situation."),
            dict(html="“Check real estate against the mandate using /awfo-q3-custody-export.xlsx.”", key="t", why="The job + source."),
            dict(html="“Then check the 10% issuer limit.”", key="t", why="Second task."),
            dict(html="“Answer in three bullet points, each under 20 words.”", key="f", why="Shape."),
            dict(html="“Calm and reassuring, but honest about any breach.”", key="o", why="Voice.")]),
    walk=dict(say="“Every strong prompt answers four questions. Let us find them.”", do=["Label each piece with the room.", "Point out: two task lines is fine.", "Submit → flag."], point="Context, Task, Format, Tone.")),
 ch("i1-summary", 3, "OUT", 150, "MODERATE", "Summarise the Thread", "Copilot summarised Reem's Al-Waha thread. Three points are wrong.", "Click the three wrong points.",
    "A fast summary only saves time if it is right.", "bec", dict(flag="KAMCO{a_summary_is_a_starting_point}", need=["date", "deck", "src"], btn="Submit the 3 wrong points →", hbtn="▾ Show thread details",
     wrongMsg="Check each point against Reem's newest message.",
     head='<div class="ph">COPILOT · SUMMARY</div><div class="pf">RE: Al-Waha FO - Q3 numbers for the family meeting · 2 messages</div>', headers="From: Reem Al-Qattan · 7–11 Oct 2026",
     body=('<div class="pbody"><p>• <span class="tl" data-k="ok1">The family wants a short memo — no slides this time.</span></p>'
           '<p>• <span class="tl" data-k="date">Deadline: Thursday 15 Oct.</span></p>'
           '<p>• <span class="tl" data-k="ok2">Check real estate against the mandate first, then the rest of the allocation and the 10% issuer limit.</span></p>'
           '<p>• <span class="tl" data-k="deck">Also prepare a 4-slide deck.</span></p>'
           '<p>• <span class="tl" data-k="src">Use the June figures if the export is late.</span></p>'
           '<p>• <span class="tl" data-k="ok3">Use the 30 Sep custody export attached.</span></p></div>')),
    walk=dict(say="“Copilot's summary looks tidy. Let us check it line by line against Reem's newest message.”",
              do=["Click Summarise on the Al-Waha thread live — compare with this version.", "Wrong: Thursday 15 Oct (now Monday 12 Oct, 1:00 pm).", "Wrong: the 4-slide deck (cancelled — memo only).", "Wrong: 'June figures' — Reem never said that. Copilot added it.", "Submit → flag."],
              point="A summary is a starting point — never the final word.")),
 ch("i1-request", 4, "OUT", 200, "MODERATE", "Read the Request", "Reem's Al-Waha thread changed the deliverable and the deadline.", "Find the final ask.",
    "Work from the newest message.", "answer", dict(flag="KAMCO{read_the_latest_first}", mail=mail_block(WAHA_THREAD), intro="Run Summarise on the thread live, then answer.",
     fields=[sel("Final deadline", ["Thu 15 Oct", "Mon 12 Oct, 1:00 pm", "Sun 11 Oct"], 1, "Newest message."),
             sel("Deliverable", ["A 4-slide deck", "A short memo only", "A deck and a memo"], 1, "Memo only — no slides."),
             sel("What to check first", ["Equity", "Real estate", "Cash"], 1, "The family is worried about property."),
             sel("Source file", ["The June factsheet", "The 30 Sep custody export", "Last year's report"], 1, "Attached 30 Sep export.")]),
    walk=dict(say="“Copilot will summarise the thread. My job is to check what changed.”", do=["Click Summarise on the Al-Waha thread.", "Run the checklist prompt.", "Answer: Mon 12 Oct 1:00 pm · memo only · real estate first · 30 Sep export."], point="The newest message wins.")),
 ch("i1-clean", 5, "XLS", 200, "MODERATE", "Clean the Export", "Clean the Al-Waha export live.", "Enter what you found.",
    "Clean first, count second.", "answer", dict(flag="KAMCO{count_rows_before_and_after}", intro="Delete the title rows, Ctrl+T, then the five cleaning prompts.",
     fields=[num("Raw data rows", W["raw_rows"], 0, "rows", "Right."), num("Duplicates removed", W["duplicates"], 0, "rows", "Right."),
             num("Holdings left", W["holdings"], 0, "holdings", "Right."), sel("Missing prices", ["NWH and GHR", "CVC and SPF", "ATLS and GTB"], 1, "Right.")]),
    walk=dict(say="“Watch the row count before and after every step.”", do=[f"Raw: {W['raw_rows']} rows.", "Highlight duplicates by Holding ID → 3 (Harbor, Bayan Telecom, Gulf Sovereign). Remove.", "Convert text quantities; clean labels; fill CVC and SPF from Price_List.", f"Left: {W['holdings']} holdings."], point="Clean before you count.")),
 ch("i1-value", 6, "XLS", 250, "HARD", "Value and Mandate", "Value, Q3 change and allocation for Al-Waha.", "Build the PivotTable and compare with the mandate.",
    "Every number must be one you can explain.", "answer", dict(flag="KAMCO{inside_the_range_or_not}", intro="USD × 0.3065 = KWD.",
     fields=[num("Total value at 30 Sep (KWD)", W["total_sep"], 1500, "KWD", "Right."), num("Q3 change (%)", W["q3_return_pct"], 0.05, "%", "Right."),
             num("Real estate weight (%)", W["alloc_pct"]["Real Estate"], 0.15, "%", "Right."), sel("Asset class outside its range", ["None", "Equity", "Fixed Income", "Real Estate", "Cash"], 3, "Real estate is below the 5% minimum.")]),
    walk=dict(say="“First the total, then the shape, then the question: inside the range or not?”", do=[f"Total {kwd(W['total_sep'])}; Q3 {W['q3_return_pct']}%.", f"PivotTable: Equity {W['alloc_pct']['Equity']}%, FI {W['alloc_pct']['Fixed Income']}%, RE {W['alloc_pct']['Real Estate']}%, Cash {W['alloc_pct']['Cash']}%.", "Real estate below 5% → breach. Equity close to 55% → mention."], point="Answer the client's question in one line.")),
 ch("i1-issuer", 7, "XLS", 250, "HARD", "Issuers and Movers", "Issuer exposure and contributors for Al-Waha.", "Sum by issuer; rank Q3 change.",
    "The whole issuer counts.", "answer", dict(flag="KAMCO{one_name_two_asset_classes}", intro="Issuer = equity + fixed income from the same name.",
     fields=[sel("Largest issuer", ["Meridian Energy", "Gulf Trade Bank", "Gulf Sovereign"], 1, "Right."), num("Its weight (%)", W["issuer_top"][0][1], 0.1, "%", "Above 10%."),
             sel("Top contributor", ["Atlas Tech Corp", "Harbor Semiconductors", "Al-Noor Bank"], 0, "Right."), sel("Bottom contributor", ["Northwind Health", "Sadaf Logistics", "Gulf Trade Bank"], 2, "Right.")]),
    walk=dict(say="“Meridian Energy has shares and a bond. Watch how the issuer total adds both.”", do=[f"Gulf Trade Bank {W['issuer_top'][0][1]}% → above 10%.", "Meridian Energy: shares + bond together.", f"Top: Atlas Tech (+{W['top3'][0][1]:,}). Bottom: Gulf Trade Bank ({W['bottom3'][0][1]:,})."], point="One name can hide in two asset classes.")),
]

# ======================= DAY 2 · TRAINEE (Al-Murjan) =======================
MD_OPTS = [dict(k="memo", label="Word memo"), dict(k="deck", label="PowerPoint deck")]
D2T = [
 ch("d2-format", 1, "WRD", 100, "EASY", "Memo or Deck?", "Five requests from KAMCO managers. Each reader needs a different format.",
    "Choose <b>memo</b> or <b>deck</b> for each. Ask: who reads it, how, and what decision?", "Amazon (2004) replaced slides in senior meetings with memos of up to six pages.",
    "assign", dict(flag="KAMCO{the_reader_picks_the_format}", opts=MD_OPTS, intro="Read alone and decide later → memo. Presented live to a group → deck.",
     items=[dict(html="The Investment Committee reads all papers at home the night before.", key="memo", why="Read alone, decided later."),
            dict(html="You present Q3 results to the Al-Murjan family in a meeting room.", key="deck", why="Live, with you presenting."),
            dict(html="Compliance needs a record of why you recommend trimming equity.", key="memo", why="A written record with reasons."),
            dict(html="The CEO wants a 10-minute update at the staff town hall.", key="deck", why="Presented to a large group."),
            dict(html="Faisal wants “one page I can read on my phone before the call”.", key="memo", why="One page, read alone.")]),
    extra='In Word, ask Copilot to turn your Al-Murjan memo into a three-bullet “phone version” Faisal can read in 30 seconds.',
    sol=dict(steps=["Memo: IC papers, Compliance record, Faisal's one page.", "Deck: the family meeting, the town hall."], point="The reader picks the format.")),
 ch("d2-blufront", 2, "WRD", 150, "MODERATE", "Answer First", "You are drafting the Al-Murjan memo in Word with Copilot.", "Choose the right content for each part of the memo, in order.",
    "Newspapers put the most important fact in the first line.", "ir", dict(flag="KAMCO{bottom_line_up_front}", phases=["Bottom line", "Evidence", "Risk", "Action"], doneMsg="Answer first, evidence next, then risk and action — a memo Faisal can read in one minute.",
     steps=[dict(phase=0, clock="Opening lines", prompt="What goes in the <b>first two sentences</b>?", options=[
              dict(t=f"The value ({kwd(M['total_sep'])}, +{M['q3_return_pct']}%), the two breaches and the recommendation.", correct=True, fb="Right — the answer and the action first."),
              dict(t="Background on the Al-Murjan family and how long they have been a client.", correct=False, fb="Faisal knows the client. Start with the answer."),
              dict(t="How you cleaned the data in Excel.", correct=False, fb="Method belongs at the end, if at all.")]),
            dict(phase=1, clock="Section 2", prompt="What comes <b>next</b>?", options=[
              dict(t="Performance and allocation against the mandate, with the numbers from your Excel table.", correct=True, fb="Right — the evidence for the bottom line."),
              dict(t="The full 22-row holdings table.", correct=False, fb="Too much. Attach it if needed."),
              dict(t="A paragraph about the Q4 market outlook in general.", correct=False, fb="Not what was asked.")]),
            dict(phase=2, clock="Section 3", prompt="Where does the <b>Al-Noor Bank</b> point go?", options=[
              dict(t=f"Issuer check: Al-Noor Bank shares + sukuk = {M['issuer_top'][0][1]}%, above the 10% limit.", correct=True, fb="Right — with the number and the limit."),
              dict(t="Leave it out — the client likes Al-Noor Bank.", correct=False, fb="A limit breach must be reported."),
              dict(t="Mention it only as a top contributor.", correct=False, fb="It is both a contributor and a breach — say both.")]),
            dict(phase=3, clock="Last section", prompt="How do you <b>end</b> the memo?", options=[
              dict(t="Recommended actions, in line with the house view: trim equity starting with Al-Noor Bank; add fixed income.", correct=True, fb="Right — clear next steps."),
              dict(t="“We expect the strong performance to continue.”", correct=False, fb="Never imply future returns."),
              dict(t="The standard client disclaimer.", correct=False, fb="This is an internal memo — no disclaimer needed.")])]),
    extra="Ask Copilot in Word to rewrite your memo's bottom line in 25 words or fewer — without changing a single number. Check that it kept them all.",
    sol=dict(steps=["Bottom line: value, change, breaches, recommendation.", "Evidence: performance and allocation.", "Risk: the Al-Noor Bank issuer breach.", "Action: trim equity / Al-Noor Bank; add fixed income."], point="Bottom line up front.")),
 ch("d2-deck", 3, "PPT", 150, "MODERATE", "Fix the Deck", "Copilot built a 5-slide deck from your memo. Three things will lose the client.",
    "Click the <b>three</b> problems. Good slides stay unclicked.", "Columbia (2003): a key warning was buried deep in a dense slide.",
    "bec", dict(flag="KAMCO{one_slide_one_message}", need=["topic", "source", "bullets"], btn="Submit the 3 problems →", wrongMsg="Not quite. Look for a title that is only a topic, a chart without a source, and a slide with too much text.",
     head='<div class="ph">DECK</div><div class="pf">AMFO-Q3-client-deck.pptx · outline view</div>', headers="5 slides · created by Copilot from AMFO-Q3-memo.docx", hbtn="▾ Show file details",
     body=('<div class="pbody">'
           f'<p><b>1.</b> <span class="tl" data-k="ok1">Your portfolio grew {M["q3_return_pct"]}% in Q3, to {kwd(M["total_sep"])}</span></p>'
           '<p><b>2.</b> <span class="tl" data-k="topic">Q3 Performance</span></p>'
           f'<p><b>3.</b> <span class="tl" data-k="ok2">Equity is {M["alloc_pct"]["Equity"]}% — above the 55% maximum</span> · <span class="tl" data-k="source">[allocation chart, no source line]</span></p>'
           '<p><b>4.</b> Al-Noor Bank is above the 10% issuer limit · <span class="tl" data-k="bullets">nine bullet points covering every holding</span></p>'
           '<p><b>5.</b> <span class="tl" data-k="ok3">We recommend trimming equity, starting with Al-Noor Bank</span></p></div>')),
    extra='Ask Copilot in PowerPoint to add an appendix slide with the full allocation table, and write speaker notes for slide 1 in Arabic.',
    sol=dict(steps=["Slide 2: a topic, not a message → write the message.", "Slide 3: add the source under the chart.", "Slide 4: cut nine bullets to three."], point="One slide, one message — and show your source.")),
 ch("d2-reply", 4, "OUT", 250, "HARD", "Check the Reply", "Copilot drafted your reply to Faisal. It took ten seconds. It has four problems.",
    "Click the <b>four</b> sentences that fail a check. Two sentences are correct.", "Deloitte Australia (2025) refunded part of a fee after AI errors reached a government report.",
    "bec", dict(flag="KAMCO{verify_before_you_send}", need=["acc", "conf", "tone", "comp"], btn="Submit the 4 problems →", wrongMsg="Not quite. Check numbers, other clients, promises and what is missing.",
     head='<div class="ph">DRAFT</div><div class="pf">To: Faisal Al-Mutairi · Cc: Noura (Compliance) · Attached: AMFO-Q3-client-deck.pptx</div>', headers="Subject: RE: FW: Al-Murjan FO - Q3 review pack", hbtn="▾ Show subject",
     body=('<div class="pbody"><p>Hi Faisal,</p>'
           f'<p><span class="tl" data-k="ok1">The client deck is attached.</span> The portfolio was worth <span class="tl" data-k="ok2">{kwd(M["total_sep"])} at 30 Sep</span>, <span class="tl" data-k="acc">up 4.6% in Q3</span>. '
           f'<span class="tl" data-k="ok3">Equity is {M["alloc_pct"]["Equity"]}%, above the 55% maximum.</span></p>'
           '<p><span class="tl" data-k="conf">I used the same format as the Al-Rumaithiya family report.</span> '
           '<span class="tl" data-k="tone">Al-Noor Bank will keep rising, so the family should not worry about the limit.</span></p>'
           '<p><span class="tl" data-k="comp">The memo will follow tomorrow.</span></p><p>Thanks</p></div>')),
    extra='Ask Copilot in Outlook to draft the client-facing version for Khalid — with the house-view disclaimer — then run the four checks on it yourself.',
    sol=dict(steps=[f"Accuracy: “up 4.6%” — it is <b>{M['q3_return_pct']}%</b>.", "Confidentiality: names another client (Al-Rumaithiya).", "Tone: promises Al-Noor Bank will rise.", "Completeness: the memo was due with the deck (Tue 3:00 pm)."],
             point="Run the four checks before every send.")),
 ch("d2-checks", 5, "OUT", 150, "MODERATE", "Name the Check", "Six problems found in KAMCO drafts last quarter.", "Match each problem to the check that catches it.",
    "Pilots run the checklist every flight.", "assign", dict(flag="KAMCO{four_checks_every_time}", opts=[dict(k="a", label="Accuracy"), dict(k="c", label="Confidentiality"), dict(k="t", label="Tone"), dict(k="m", label="Completeness")],
     intro="Accuracy = the numbers. Confidentiality = the people. Tone = the voice and promises. Completeness = everything asked for.",
     items=[dict(html="The deck says equity is 16.0%; the analysis says 61.0%.", key="a", why="A wrong number."),
            dict(html="The reply went to the whole family distribution list, including a cousin outside the mandate.", key="c", why="Wrong people."),
            dict(html="“This fund is guaranteed to beat the market.”", key="t", why="A promise — never."),
            dict(html="The client deck has no disclaimer.", key="m", why="Client documents need the standard disclaimer."),
            dict(html="The email says “see attached” but nothing is attached.", key="m", why="Missing part of the deliverable."),
            dict(html="A one-line reply to a long, formal letter from the family CFO.", key="t", why="Does not match the reader.")]),
    extra='Write your own reply with three planted errors (one per check) and swap with your neighbour. Who finds all three first?',
    sol=dict(steps=["Accuracy: 16.0% vs 61.0%.", "Confidentiality: wrong recipients.", "Tone: the guarantee; the one-line reply.", "Completeness: no disclaimer; no attachment."], point="Accuracy · Confidentiality · Tone · Completeness.")),
 ch("d2-agent", 6, "AGT", 200, "MODERATE", "Build the Agent", "You will build a Request Triage Assistant in Copilot Agent Builder.", "Make the right call at each step of the build.",
    "Klarna (2024–25): an AI assistant took two-thirds of chats — then the company made sure customers can still reach a human.",
    "ir", dict(flag="KAMCO{instructions_make_the_agent}", phases=["Describe", "Instruct", "Knowledge", "Test", "Share"], doneMsg="Described, instructed, grounded, tested and fixed — an agent you can trust with the repeat work.",
     steps=[dict(phase=0, clock="Create agent", prompt="What is the best <b>description</b>?", options=[
              dict(t="Reads a client request and returns the client, outputs, deadline, people to copy and risks.", correct=True, fb="Clear, single job."),
              dict(t="Helps with everything in wealth management.", correct=False, fb="Too broad — it will do nothing well."),
              dict(t="An AI agent.", correct=False, fb="Says nothing about the job.")]),
            dict(phase=1, clock="Instructions", prompt="Which instruction prevents the Al-Murjan mistake?", options=[
              dict(t="“Always use the newest message when instructions change.”", correct=True, fb="Right — that is the rule people forget."),
              dict(t="“Be helpful and friendly.”", correct=False, fb="Nice, but it does not change the result."),
              dict(t="“Use your best judgement.”", correct=False, fb="Judgement is yours. Give the agent rules.")]),
            dict(phase=2, clock="Knowledge", prompt="Which file do you add as <b>knowledge</b>?", options=[
              dict(t="The house view (with the client communication rules).", correct=True, fb="The agent can now flag rule breaks."),
              dict(t="Every client's custody export.", correct=False, fb="It does not need client data to triage requests."),
              dict(t="Nothing — it knows enough.", correct=False, fb="Without your rules, it cannot check them.")]),
            dict(phase=3, clock="Test", prompt="You paste the Al-Murjan thread. It says the deadline is Wednesday. Next?", options=[
              dict(t="Fix the instructions, then test again.", correct=True, fb="Test, fix, re-test."),
              dict(t="Share it anyway — it is close.", correct=False, fb="A wrong deadline is not close."),
              dict(t="Delete it.", correct=False, fb="One fix is faster.")]),
            dict(phase=4, clock="Share", prompt="It passes your tests. Who do you share it with first?", options=[
              dict(t="Two colleagues, to try it on real requests for a week.", correct=True, fb="Start small, learn, then widen."),
              dict(t="The whole firm today.", correct=False, fb="Pilot first."),
              dict(t="Clients, so they can triage their own requests.", correct=False, fb="Internal tool, internal users.")])]),
    extra="If Agent Builder is on for you: add two starter prompts to your agent and one rule that makes it refuse to share another client's data. Test it with Khalid's request.",
    sol=dict(steps=["Describe one clear job.", "Instruction: always use the newest message.", "Knowledge: the house view rules.", "Test → fix → re-test.", "Share with a small pilot group."], point="An agent is only as good as its instructions.")),
]

# ======================= DAY 2 · INSTRUCTOR (Al-Waha) =======================
D2I = [
 ch("i2-format", 1, "WRD", 100, "EASY", "Memo or Deck?", "Five different requests.", "Memo or deck for each.", "The reader picks the format.",
    "assign", dict(flag="KAMCO{who_reads_it_and_how}", opts=MD_OPTS, intro="Read alone → memo. Presented live → deck.",
     items=[dict(html="Reem asks for the Al-Waha Q3 update “memo only, no slides”.", key="memo", why="The request says so."),
            dict(html="A pitch to a new family office in their majlis.", key="deck", why="Live presentation."),
            dict(html="A note to the board's risk committee explaining an issuer breach.", key="memo", why="Read and decided later."),
            dict(html="A 15-minute training for new RMs.", key="deck", why="Presented."),
            dict(html="A file note recording the client's instruction.", key="memo", why="A record.")]),
    walk=dict(say="“Before Copilot writes a word, decide the format.”", do=["Ask: who reads it, how, what decision?", "Sort all five.", "Submit → flag."], point="The reader picks the format.")),
 ch("i2-blufront", 2, "WRD", 150, "MODERATE", "Answer First", "Draft the Al-Waha memo live.", "Choose the right content for each part.", "Bottom line up front.",
    "ir", dict(flag="KAMCO{answer_then_evidence}", phases=["Bottom line", "Evidence", "Action"], doneMsg="Answer, evidence, action.",
     steps=[dict(phase=0, clock="First lines", prompt="First two sentences?", options=[dict(t=f"Value {kwd(W['total_sep'])}, +{W['q3_return_pct']}%; real estate below range; Gulf Trade Bank above 10%; recommendation.", correct=True, fb="Answer first."), dict(t="A history of the family's portfolio.", correct=False, fb="Not first.")]),
            dict(phase=1, clock="Middle", prompt="Evidence?", options=[dict(t="Allocation table vs mandate, issuer table.", correct=True, fb="Right."), dict(t="Market news.", correct=False, fb="Not asked.")]),
            dict(phase=2, clock="End", prompt="End with?", options=[dict(t="Actions in line with the house view.", correct=True, fb="Right."), dict(t="A return forecast.", correct=False, fb="Never.")])]),
    walk=dict(say="“I will write the bottom line before anything else.”", do=["Paste the Al-Waha summary table into the Word prompt.", "Reference /house-view-q4-2026.docx.", "Choose the answers aloud."], point="Answer first.")),
 ch("i2-deck", 3, "PPT", 150, "MODERATE", "Fix the Deck", "A Copilot deck for Al-Waha with three problems.", "Click the three.", "One slide, one message.",
    "bec", dict(flag="KAMCO{titles_tell_the_story}", need=["topic", "source", "bullets"], btn="Submit the 3 problems →", wrongMsg="Topic title, missing source, too much text.",
     head='<div class="ph">DECK</div><div class="pf">AWFO-Q3-deck.pptx · outline view</div>', headers="4 slides · created by Copilot from AWFO-Q3-memo.docx", hbtn="▾ Show file details",
     body=('<div class="pbody">'
           f'<p><b>1.</b> <span class="tl" data-k="ok1">Al-Waha grew {W["q3_return_pct"]}% in Q3, to {kwd(W["total_sep"])}</span></p>'
           '<p><b>2.</b> <span class="tl" data-k="topic">Asset Allocation</span></p>'
           '<p><b>3.</b> <span class="tl" data-k="ok2">Gulf Trade Bank is above the 10% issuer limit</span> · <span class="tl" data-k="source">[issuer chart with no source]</span></p>'
           '<p><b>4.</b> Recommendation · <span class="tl" data-k="bullets">eleven bullet points</span></p></div>')),
    walk=dict(say="“Read only the titles. Do they tell the story?”", do=["Click slide 2's title — a topic.", "Click slide 3's chart — no source.", "Click slide 4 — eleven bullets.", "Submit → flag."], point="Titles tell the story.")),
 ch("i2-reply", 4, "OUT", 250, "HARD", "Check the Reply", "The Al-Waha reply to Reem.", "Click the four problems.", "Verify before you send.",
    "bec", dict(flag="KAMCO{you_sign_it_not_copilot}", need=["acc", "conf", "tone", "comp"], btn="Submit the 4 problems →", wrongMsg="Numbers, other clients, promises, missing items.",
     head='<div class="ph">DRAFT</div><div class="pf">To: Reem Al-Qattan · Attached: AWFO-Q3-memo.docx</div>', headers="Subject: RE: Al-Waha FO - Q3 numbers", hbtn="▾ Show subject",
     body=('<div class="pbody"><p>Dear Reem,</p>'
           f'<p><span class="tl" data-k="ok1">Total value at 30 Sep was {kwd(W["total_sep"])}.</span> <span class="tl" data-k="acc">Real estate is 5.4%, inside the mandate.</span></p>'
           '<p><span class="tl" data-k="conf">This matches what we saw for the Al-Murjan family.</span> <span class="tl" data-k="tone">We are confident returns will stay strong.</span></p>'
           '<p><span class="tl" data-k="comp">The issuer table will follow next week.</span></p></div>')),
    walk=dict(say="“Copilot wrote this in ten seconds. Let us spend one minute checking it.”", do=["Accuracy: 5.4% → it is 4.5%, below 5%.", "Confidentiality: Al-Murjan named.", "Tone: promise of returns.", "Completeness: issuer table missing."], point="You sign it, not Copilot.")),
 ch("i2-checks", 5, "OUT", 150, "MODERATE", "Name the Check", "Five more problems.", "Match each to a check.", "Four checks.",
    "assign", dict(flag="KAMCO{one_minute_before_send}", opts=[dict(k="a", label="Accuracy"), dict(k="c", label="Confidentiality"), dict(k="t", label="Tone"), dict(k="m", label="Completeness")], intro="Match each.",
     items=[dict(html="Q3 change shown as +12.9% instead of +1.29%.", key="a", why="Number."), dict(html="The family's private email copied to an outside broker.", key="c", why="People."),
            dict(html="“No risk at all in this bond.”", key="t", why="Promise."), dict(html="Reem asked for real estate first; it is missing.", key="m", why="Missing part."),
            dict(html="A casual “hey guys” to the family patriarch.", key="t", why="Voice.")]),
    walk=dict(say="“Name the check that would have caught it.”", do=["Match each item.", "Submit → flag."], point="One minute before send.")),
 ch("i2-agent", 6, "AGT", 200, "MODERATE", "Build the Agent", "Build a Mandate Check Assistant live.", "Make the right call at each step.", "Test before you trust.",
    "ir", dict(flag="KAMCO{test_before_you_trust}", phases=["Describe", "Instruct", "Test"], doneMsg="A small, tested agent.",
     steps=[dict(phase=0, clock="Describe", prompt="Best description?", options=[dict(t="Checks a pasted allocation table against the mandate ranges and the 10% issuer limit.", correct=True, fb="One job."), dict(t="Does portfolio management.", correct=False, fb="Too broad.")]),
            dict(phase=1, clock="Instructions", prompt="Key instruction?", options=[dict(t="“Count shares and bonds from the same issuer together.”", correct=True, fb="The rule people miss."), dict(t="“Be accurate.”", correct=False, fb="Not testable.")]),
            dict(phase=2, clock="Test", prompt="It misses the Gulf Trade Bank breach. Next?", options=[dict(t="Fix the instruction, re-test with the Al-Waha table.", correct=True, fb="Right."), dict(t="Share it.", correct=False, fb="Not yet.")])]),
    walk=dict(say="“I will build it in Agent Builder now — watch the Instructions box.”", do=["Copilot app → Agents → Create agent.", "Describe; paste instructions; add the house view as knowledge.", "Test with the Al-Waha allocation table; fix; re-test."], point="Test before you trust.")),
]

WELCOME = {
 ("trainee", 1): {"eyebrow": "KAMCO · Day 1", "title": "From Inbox", "titleG": "to Insight", "sub": "Seven challenges on the Al-Murjan request — safe use, prompting, summarising and reading the thread, cleaning the export and checking the mandate. Some happen here; some happen in Copilot with your files."},
 ("instructor", 1): {"eyebrow": "Day 1 · Instructor demo", "title": "Demo", "titleG": "Day 1", "sub": "The Al-Waha scenario — parallel to the trainee lab — with the solution walkthrough on screen."},
 ("trainee", 2): {"eyebrow": "KAMCO · Day 2", "title": "From Analysis", "titleG": "to Reply", "sub": "Six challenges — choosing the format, writing answer-first, fixing the deck, checking the reply and building an agent."},
 ("instructor", 2): {"eyebrow": "Day 2 · Instructor demo", "title": "Demo", "titleG": "Day 2", "sub": "The Al-Waha scenario — parallel to the trainee lab — with the solution walkthrough on screen."},
}
LABS = {("trainee", 1): D1T, ("instructor", 1): D1I, ("trainee", 2): D2T, ("instructor", 2): D2I}
