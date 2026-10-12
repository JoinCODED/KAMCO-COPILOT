"""Day 1 trainee lab — task format (MCIM lab engine), KAMCO content, no tracks."""
import json
import emails
A = json.load(open("out/answers.json"))
M = A["murjan"] if "murjan" in A else A
THREAD = emails.thread_text(emails.MURJAN_THREAD)
COP = '<a href="https://copilot.cloud.microsoft/" target="_blank" rel="noopener">copilot.cloud.microsoft</a>'
FILES = [{"label": "amfo-q3-custody-export.xlsx · Al-Murjan custody export (30 Sep)", "href": "amfo-q3-custody-export.xlsx",
          "note": "Save it to your <b>OneDrive</b>, open it in Excel for the web or desktop, and turn on <b>AutoSave</b>. Copilot in Excel needs that."}]

TASKS = [
 dict(id="E1.1", app="Copilot Chat", title="First contact", minutes="5 min", block="Block 1",
      scenario="Your first real win. Pick any starter that fits your work, tap to copy, replace the [brackets], and run it. The bar is simple: <b>would you use the result?</b>",
      steps=[f"Open Copilot Chat at {COP} and start a <b>New chat</b>. Sign in with your <b>KAMCO work account</b> (or the CODED account on your card).",
             "Pick <b>one</b> starter below and tap it to copy. Replace the [brackets] with your own details — nothing confidential, no real client names.",
             "Read the result. Would you use it? If not, tell Copilot what to change — don't start again."],
      starters=["Explain [a term from your work, e.g. duration, NAV, rebalancing] in two sentences, like I'm new here.",
                "Draft a three-line message telling my team our 10 AM portfolio review moved to 11 AM.",
                "Give me five polite ways to tell a client their documents are still being processed.",
                "Turn these rough notes into three clear bullet points: [paste your notes]",
                "Rewrite this to sound more professional and polite: [paste your sentence]",
                "Summarise what this email asks me to do, in one line: [paste an email with no confidential details]",
                "Suggest three subject lines for an email inviting clients to our Q4 market outlook session.",
                "Give me a checklist for [a routine task you do, e.g. onboarding a new client account], so I don't miss a step."],
      expect="A result you would actually use — your first win to share with the room.",
      stretch="Steer it without rewriting your prompt: <i>“Make it shorter.”</i> → <i>“Make it warmer.”</i> → <i>“Now write it in Arabic.”</i>",
      boss="Ask for a version for a client who has already complained twice about slow reporting. What changed in the tone — and did Copilot promise something you can't deliver?"),
 dict(id="E1.2", app="Your week", title="Your time audit", minutes="5 min", block="Block 1",
      scenario="Where does your week go? Remember the ice-breaker wall. List three tasks that drain your time. Tag each one with what AI does best — <b>Generate, Condense, Find or Transform</b> — and guess the hours. <b>You will build a prompt for one of them in Block 2.</b>",
      steps=["Need ideas? Run the helper prompt in Copilot Chat. Replace the [brackets] first.",
             "Fill in three tasks from <b>your</b> real week. Add a tag and a rough number of hours per week."],
      prompt="I work as a [your job title] in [wealth management / operations / your department] at an investment company in Kuwait. List 10 tasks in a typical week where AI could save me time. Group them under four headings: Generate, Condense, Find, Transform. One line each.",
      widget="timeaudit",
      expect="Three real tasks, tagged, with hours. The biggest one is the task you will write a prompt for in E1.5.",
      stretch="Ask Copilot: <i>“Break this task into steps: [your biggest task]. Which steps could Copilot do, and which must I do myself?”</i>",
      boss="Multiply your three tasks' hours by 46 working weeks. That is your yearly “drag”. What would you do with half of it back?"),
 dict(id="E1.3", app="Judgement", title="Safe or not?", minutes="5 min", block="Block 1",
      scenario="Your KAMCO work account gives you enterprise data protection. That does not mean everything belongs in a prompt. <b>Share only what the task needs, and only with your work account.</b>",
      steps=["Read the five items below.", "For each one, decide: <b>Fine</b> in work Copilot · <b>Fine after removing personal data</b> · <b>Never</b>.", "Write your answer in each box, then open “Check your findings”."],
      findings=[{"label": "1. The 30 Sep custody export for Al-Murjan Family Office — your client — to analyse it.", "hint": "Fine / After removing personal data / Never"},
                {"label": "2. A client complaint email with the client's mobile number and civil ID — you want a summary of the complaint.", "hint": "Fine / After removing personal data / Never"},
                {"label": "3. The Q4 2026 House View from the research portal.", "hint": "Fine / After removing personal data / Never"},
                {"label": "4. Your KAMCO password, so Copilot can log in to a portal for you.", "hint": "Fine / After removing personal data / Never"},
                {"label": "5. Al-Murjan's holdings pasted into a free public chatbot on your personal phone.", "hint": "Fine / After removing personal data / Never"}],
      reveal="<b>1 Fine</b> — your client, your task, your work tenant. <b>2 After removing personal data</b> — the summary does not need the civil ID or phone number; replace them with placeholders. <b>3 Fine</b> — internal, inside KAMCO's boundary, needed for the task. <b>4 Never</b> — never share passwords with any tool or person. <b>5 Never</b> — no enterprise data protection; client data never goes there.",
      expect="Five items sorted — and one rule you can say out loud: <b>even inside a safe tool, share only what the task needs.</b>",
      stretch="In Copilot Chat (work account), ask: <i>“What should staff at an investment firm never paste into an AI tool? Give five examples.”</i> Compare with your answers.",
      boss="Samsung (2023): staff pasted confidential code into a public chatbot three times in twenty days. Write the one-line rule you would put on a sticky note for your team."),
 dict(id="E1.4", app="Copilot Chat", title="From zero to hero", minutes="10 min", block="Block 2 · CTFT",
      scenario="One weak prompt, four rounds. Each round adds one CTFT ingredient. Run it each time and rate the result. Rounds 0–1 with the room, rounds 2–4 on your own.",
      steps=["Start a <b>New chat</b>. Run Round 0 on its own.",
             "For each round, copy the new line and add it to your prompt — or run the full Round 4 prompt at the end.",
             "Rate each result from 1 to 5. Which ingredient made the biggest jump?"],
      widget="zth",
      rounds=[{"label": "The weak prompt", "text": "Write an email to a client."},
              {"label": "+ Context", "text": "I am a relationship manager at an investment company in Kuwait. Our client, the CFO of a family office, asked how much of their portfolio is now with one bank. After a strong quarter, that bank's shares and sukuk together are 12.2% of the portfolio — above the 10% single-issuer limit in their mandate."},
              {"label": "+ Task", "text": "Write him an email that answers his question and proposes we discuss reducing the position at our meeting on Wednesday."},
              {"label": "+ Format", "text": "Keep it under 120 words, with the 12.2% figure in the first two lines."},
              {"label": "+ Tone & limits", "text": "Clear and calm, for a family CFO. No jargon. Do not recommend a specific trade and do not promise returns. Sign off as the Wealth Management team."}],
      expect="Five results, five ratings — and one sentence on which ingredient made the biggest difference.",
      stretch="Steer, don't rewrite: <i>“Make it 20% shorter.”</i> → <i>“Now a WhatsApp version.”</i> → <i>“Now in Arabic, same tone.”</i>",
      boss="The hard client: he is worried, he asks why nobody warned him earlier, and he wants you to sell today. Get an email that explains the limit, does not blame anyone, agrees a next step for Wednesday, stays under 150 words — and promises nothing you can't deliver."),
 dict(id="E1.5", app="Copilot Chat", title="Build your own prompt", minutes="10 min", block="Block 2 · CTFT",
      scenario="Now build one for <b>your own job</b>. Role and Context set the scene. Task says what to do. Format and Tone shape it. Add a Source (a file) and an Example if you have them.",
      steps=["Pick a real, repeating task — one from your E1.2 time audit or the ice-breaker wall. Leave out confidential details.",
             "Fill the builder. Stuck? Tap <b>Load the example</b>.",
             "Copy the prompt and run it in Copilot Chat. Did the role and context show up in the answer?",
             "Improve it once. Keep the final version — paste it in the result box below."],
      widget="builder",
      examples={"sales": {"role": "You are a senior relationship manager in wealth management at an investment company in Kuwait.",
                          "ctx": "A family office client meets us next week. Their portfolio is up 2.5% in Q3, but equities are now 61% against a 55% mandate maximum.",
                          "task": "Draft the three points I should open the meeting with.",
                          "fmt": "Three numbered points, one or two sentences each, under 120 words in total.",
                          "tone": "Calm, clear and factual. No jargon. Do not promise returns or recommend specific trades."}},
      expect="One prompt you will reuse — tested in Copilot and saved.",
      stretch="Fill the Example field — paste a short sample you like — and run it again. One example changes the structure and voice. (This is called few-shot prompting.)",
      boss="One prompt, two readers: ask for two versions in one go — one for your manager, one for a client. Same facts, different tone."),
 dict(id="E1.6", app="Outlook", title="Tame the thread — then reply", minutes="15 min", block="Block 3 · Outlook", writeOwn=True,
      scenario="Faisal's thread has three messages, and the instructions changed twice. Get the picture, find what is really being asked — then reply to Faisal.",
      steps=["Find the email <b>RE: FW: Al-Murjan FO - Q3 review pack</b> in your inbox. Not there? Copy the thread below, send it to yourself with that subject — or paste it straight into Copilot Chat.",
             "Open the email. Select <b>Summary by Copilot</b> at the top — or write your prompt for goal 1 in the Copilot pane.",
             "Write your prompt for goal 2 to draft the reply. Then steer the tone twice: <i>“shorter”</i>, <i>“a little warmer”</i>. Don't retype.",
             "Before you send: write your prompt for goal 3, or use <b>Coaching by Copilot</b>, to check tone and clarity. Would you send it?"],
      fallback="No Summary by Copilot button? Paste the thread into the Copilot pane in Outlook — or into Copilot Chat — and work through the same goals.",
      briefs=[{"label": "Thread · RE: FW: Al-Murjan FO - Q3 review pack", "text": THREAD}],
      prompts=[{"label": "1 · Summarise", "goal": "Get the picture fast: the final deadline, the meeting, each deliverable and its format, who to copy — and anything you should <b>not</b> do.",
                "text": "Summarise this thread. List the final deadline, the client meeting date and time, each deliverable and its format, who I must copy, and any request I should not do. Use the newest message when instructions change."},
               {"label": "2 · Draft the reply", "goal": "Reply to Faisal: confirm the new deadline and the two deliverables, and say you will not send the Al-Rumaithiya report (it is another client's data) — suggest a blank template instead.",
                "text": "Draft my reply to Faisal. Confirm I will send the 5-slide client deck and the one-page memo by Tuesday 13 Oct, 3:00 pm, using the 30 Sep custody export, and that I will copy Noura in Compliance. Say we cannot share the Al-Rumaithiya family report because it is another client's data, and offer a blank sample of our report format instead. Under 120 words. Polite and direct."},
               {"label": "3 · Check before sending", "goal": "Before you send: is it clear, is the tone right for an MD, and does it cover the deadline, both deliverables and the declined request?",
                "text": "Check my reply: is it clear, is the tone right for a managing director, and does it cover the deadline, both deliverables, who I copy and the request I am declining?"}],
      findings=[{"label": "Final deadline for your pack", "hint": "day, date and time"}, {"label": "Client meeting", "hint": "day, date and time"},
                {"label": "Deliverables and format", "hint": "what, and how many slides / pages"}, {"label": "Who must be copied", "hint": "name and team"},
                {"label": "The request you should decline — and why", "hint": ""}],
      reveal="<b>Deadline:</b> Tuesday 13 Oct, 3:00 pm (not Wednesday — the newest message wins). <b>Meeting:</b> Wednesday 14 Oct, 11:00. <b>Deliverables:</b> a 5-slide client deck and a one-page memo for Faisal, built from the <b>30 Sep custody export</b> (not the June factsheet). <b>Copy:</b> Noura in Compliance before anything goes to the client. <b>Decline:</b> sending the Al-Rumaithiya family report — it is another client's data.<br><br><b>Common Copilot slips to check for:</b> the old Wednesday deadline, “use the June factsheet”, or listing the Al-Rumaithiya report as an action. If your summary has any of these, it mixed old and new instructions.",
      expect="A summary that has the <b>newest</b> deadline and source — and a reply that confirms the work, copies Compliance and politely declines the other client's report.",
      stretch="Ask: <i>“Draft a two-line reply to Khalid confirming Wednesday 11:00 and saying the pack will cover the Al-Noor Bank exposure and the equity mandate.”</i> Then run Coaching by Copilot on it.",
      boss="Ask Copilot: <i>“What is missing from this thread that the client will ask about on Wednesday?”</i> Add one line to your reply if it matters."),
 dict(id="E1.7", app="Excel", title="Clean the export", minutes="15 min", block="Block 4 · Excel", files=FILES,
      scenario="The Al-Murjan custody export has duplicates, numbers stored as text, missing prices and messy labels. <b>Clean first. Count second.</b>",
      steps=["Open the export from OneDrive. On <b>Holdings_Export</b>, delete the title rows above the headers, click in the data and press <b>Ctrl+T</b>.",
             "Run the five prompts below in Copilot in Excel, <b>in order</b>. Check the result after each one.",
             "Record what you found, then open “Check your findings”."],
      prompts=[{"label": "1 · Duplicates", "text": "Highlight duplicate rows in this table based on Holding ID."},
               {"label": "2 · Text to numbers", "text": "Convert the Quantity column to numbers. Some values are stored as text with commas."},
               {"label": "3 · Clean labels", "text": "Add a column called Asset Class (clean) that maps equities, EQ and Equity to Equity; FI, Bonds and fixed income to Fixed Income; REIT to Real Estate; Cash & Deposits and cash to Cash."},
               {"label": "4 · Fill missing prices", "text": "Add a column called Price 30 Sep (filled). Use Price 30-Sep-2026. If it is blank, look up the Ticker in the Price_List sheet. Trim spaces from the Ticker first."},
               {"label": "5 · Market value", "text": "Add a column Market Value KWD = Quantity × Price 30 Sep (filled) × the rate to KWD from the FX_Rates sheet (USD = 0.3065, KWD = 1). Show me the formula."}],
      findings=[{"label": "Data rows in the raw export (below the headers)", "hint": "rows"}, {"label": "Duplicate rows removed", "hint": "rows"},
                {"label": "Holdings left after cleaning", "hint": "holdings"}, {"label": "The two tickers with a missing 30 Sep price", "hint": "tickers"}],
      reveal="<b>26</b> raw rows · <b>4</b> duplicates (Atlas Tech, Gulf Trade Bank, US Treasury 2030, Failaka Foods) · <b>22</b> holdings left · missing prices: <b>NWH</b> and <b>GHR</b> — filled from Price_List.",
      expect="Row count checked before and after every step. 22 clean holdings with a Market Value KWD column.",
      stretch="Ask Copilot in Excel: <i>“Which columns still have inconsistent values?”</i> Then fix the <b>Price Date</b> column so every value is a real date.",
      boss="Ask Copilot to explain the Market Value formula in plain English. Then test one row by hand with a calculator. Does it match?"),
 dict(id="E1.8", app="Excel", title="Value and mandate", minutes="10 min", block="Block 5 · Excel", files=FILES,
      scenario="Faisal's first two questions: <b>what is the portfolio worth, and are we inside the mandate?</b> Remember: USD × 0.3065 = KWD. Q3 change = value at 30 Sep minus value at 30 Jun (quantities did not change).",
      steps=["Work in your cleaned table from E1.7.", "Run the prompt below. Compare the result with the <b>Mandate</b> sheet.", "Record what you found, then open “Check your findings”."],
      prompt="Create a PivotTable of Market Value KWD by Asset Class (clean), with each value as a % of the grand total. Add the Min and Max from the Mandate sheet and a column that says BREACH if the weight is outside the range.",
      findings=[{"label": "Total portfolio value at 30 Sep (KWD)", "hint": "no decimals"}, {"label": "Q3 change (%)", "hint": "two decimals"},
                {"label": "Equity weight at 30 Sep (%)", "hint": "one decimal"}, {"label": "Which asset class is outside its mandate range?", "hint": ""}],
      reveal="Total: <b>KWD 4,696,424</b> (with duplicates it would be KWD 5,785,022 — wrong). Q3 change: <b>KWD 112,674 = 2.46%</b>. Allocation: Equity <b>61.0%</b>, Fixed Income 22.8%, Real Estate 8.3%, Cash 7.9%. Breach: <b>Equity</b> — above the 55% maximum.",
      expect="Every number explained — and one line Faisal can use: <i>“Equity is 61.0%, above the 55% mandate maximum.”</i>",
      stretch="Add a column that shows how far each asset class is from its mandate minimum or maximum, in percentage points. Then ask Copilot to chart allocation against target.",
      boss="Ask Copilot to write the mandate finding in one sentence for the client. Check every number in it against your PivotTable."),
 dict(id="E1.9", app="Excel", title="Issuers and movers", minutes="10 min", block="Block 5 · Excel", files=FILES,
      scenario="Khalid asked how much of the portfolio sits with Al-Noor Bank. Faisal wants the top and bottom contributors. <b>The issuer limit counts the whole issuer — shares and bonds together.</b>",
      steps=["Work in your cleaned table.", "Run the two prompts below.", "Record what you found, then open “Check your findings”."],
      prompts=[{"label": "1 · Issuer exposure", "text": "Sum Market Value KWD by Issuer, excluding cash. Show each issuer as a % of the total portfolio value, sorted from largest to smallest. Highlight any issuer above 10%."},
               {"label": "2 · Movers", "text": "Add a column Q3 Change KWD = Quantity × (Price 30 Sep (filled) − Price 30-Jun-2026) × rate to KWD. Show the top 3 and bottom 3 holdings by Q3 Change KWD."}],
      findings=[{"label": "Largest issuer and its weight (%)", "hint": "name and %"}, {"label": "Top contributor in Q3 (KWD)", "hint": ""}, {"label": "Bottom contributor in Q3 (KWD)", "hint": ""}],
      reveal="<b>Al-Noor Bank</b> shares + sukuk = <b>12.21%</b> → above the 10% limit. Top 3: Al-Noor Bank (+38,640), Atlas Tech Corp (+32,955), Harbor Semiconductors (+31,447). Bottom 3: Sadaf Logistics (−24,300), Gulf Horizon REIT (−10,360), Northwind Health (−7,552).",
      expect="The issuer breach found — with shares and sukuk counted together — and the movers ready for the deck.",
      stretch="Ask Copilot: <i>“How much of Al-Noor Bank (in KWD) would we need to sell to bring it back to 10% of the portfolio?”</i> Check its maths by hand — you should get about KWD 104,000.",
      boss="Ask Copilot to write three findings for Faisal, one line each. Check every number against your tables before you send them."),
]


def build(out_path, back="coded-kamco-day-1.html", tasks=None, day=1, chip="Day 1 · From Inbox to Insight", key="kamco_copilot_day1_tasks", site=None):
    s = open("templates/mcim-lab.html", encoding="utf-8").read()
    i = s.index("window.LAB = {"); j = s.index("\n};", i) + 3
    data = "window.LAB = " + json.dumps({"day": "Day %d" % day, "key": key, "tasks": tasks or TASKS}, ensure_ascii=False, indent=1) + ";"
    s = s[:i] + data + s[j:]
    rep = [
        ('<script src="site-config.js"></script>', '<script>window.SITE=%s;</script>' % json.dumps(site or {})),
        ('<span class="day-chip">Day 1 · Meet the Engine</span>', '<span class="day-chip">%s</span>' % chip),
        ('<a class="back" href="coded-copilot-day-1.html">', '<a class="back" href="%s">' % back),
        ('<a href="before-you-start.html">Setup help</a>', '<a href="case-files.html">Case files</a>'),
        ('Load the example for my track', 'Load the example'),
        ('Catering apology (Round 4)', 'Client email (Round 4)'),
        ('Biggest one = your capstone candidate on Thursday.', 'Biggest one = the task you build a prompt for in E1.5.'),
        ('Worth keeping? Paste it into your Prompt Bank in Word.', 'Worth keeping? Save it in your own notes.'),
        ('e.g. writing the weekly sales update', 'e.g. preparing the monthly client report'),
    ]
    for a, b in rep:
        assert a in s, a
        s = s.replace(a, b)
    # no tracks: drop the track picker, the prompt-bank pill and the track row in the time audit
    import re
    s = re.sub(r'<div class="role-pick">.*?</div>\n', '', s, count=1, flags=re.S)
    s = re.sub(r'<a class="pbpill".*?</a>\n', '', s, count=1, flags=re.S)
    old = "'<div class=\"ta-role\"><span>Your track for the three days:</span>' + Object.keys(ROLES).map(function(k){ return '<button type=\"button\" class=\"ta-r' + (role() === k ? ' on' : '') + '\" data-r=\"' + k + '\">' + ROLES[k] + '</button>'; }).join('') + '</div>' +"
    assert old in s
    s = s.replace(old, "")
    s = re.sub(r"<title>.*?</title>", "<title>Day %d Lab — AI at Work with Microsoft Copilot · CODED × KAMCO</title>" % day, s, count=1)
    s = s.replace("Mastering Copilot in Microsoft 365", "AI at Work with Microsoft Copilot")
    open(out_path, "w", encoding="utf-8").write(s)


if __name__ == "__main__":
    build("out/site/coded-kamco-day-1-lab.html")
    print("task lab day 1:", len(TASKS), "tasks")
