"""Capstone task (E2.10) for the Day 2 lab: pick a field; seven steps from email to reply."""
import json

FIELDS = {"wm": "Wealth Management", "am": "Asset Management", "rs": "Investment Research", "ops": "Operations", "fin": "Finance", "hr": "Human Resources", "lc": "Legal & Compliance"}
HV = {"label": "house-view-q4-2026.docx · number format, client rules and the standard disclaimer", "href": "house-view-q4-2026.docx",
      "note": "<b>Grounding file</b> for the brief and the deck: section 4 (rules for client communication) and section 5 (disclaimer)."}

SPEC = {
 "wm": dict(
   scenario="You are a <b>portfolio analyst in Wealth Management</b>. The Investment Committee wants a Q3 review of <b>Al-Bayan Holding</b> — and the deadline just moved. You will brief the Committee internally <b>and</b> give the relationship manager a client deck.",
   xlsx=("abh-q3-custody-export.xlsx", "Al-Bayan Holding custody export, 30 Sep — Holdings_Export, Price_List, FX_Rates, Mandate"),
   clean=["Highlight duplicate rows in this table based on Holding ID. Then remove them and tell me how many rows are left.",
          "Convert the Quantity column to numbers. Add a column Asset Class (clean) that maps every label to Equity, Fixed Income, Real Estate or Cash.",
          "Add a column Price 30 Sep (filled): use Price 30-Sep-2026, and if it is blank look up the Ticker in the Price_List sheet. Then add Market Value KWD = Quantity × Price 30 Sep (filled) × the rate to KWD from FX_Rates."],
   analyse=["Give me the total Market Value KWD at 30 Sep and at 30 Jun (use Price 30-Jun-2026 the same way), and the Q3 change in KWD and %.",
            "Create a PivotTable of Market Value KWD by Asset Class (clean) as a % of the total. Add the Min and Max from the Mandate sheet and a column that says BREACH if the weight is outside the range.",
            "Sum Market Value KWD by Issuer, excluding cash, as a % of the total portfolio. Highlight any issuer above 10%. Then show the top 3 and bottom 3 holdings by Q3 change in KWD."],
   findings=[("Total value 30 Sep (KWD)", ""), ("Q3 change (KWD and %)", ""), ("Asset class outside its mandate range", ""), ("Issuer above 10%", ""), ("Top and bottom contributor", "")],
   chart="Create a clustered bar chart of each asset class weight next to its mandate Min and Max. Title it with the message, for example “Real estate is above its mandate range”.",
   brief_to="Huda Al-Enezi for the Investment Committee (internal — no client disclaimer)",
   deck_for="Yousef Al-Kandari to use with the client (client-facing — add the standard disclaimer, never another client's data)",
   brief_sections="Bottom line (2 lines) · Key numbers table (value, Q3 change, allocation vs mandate, issuer check) · What drove the quarter (top and bottom 3) · Recommendation · Next steps",
   deck_slides="1 The message in one line · 2 Value and Q3 change · 3 Allocation vs mandate (your chart) · 4 Concentration: the issuer check · 5 What drove the quarter · 6 Recommendation and next steps — then the disclaimer",
   decline="Fahad asked for the Al-Murjan family's results. Your reply must say you cannot share another client's data.",
   stretch="Ask Copilot in Excel: <i>“How much of the largest real estate holding would we need to sell to bring real estate back to 15%?”</i> Check its maths by hand and add one line to the brief.",
   boss="Write a three-line WhatsApp-length version of the recommendation that Yousef could say out loud to the client. No numbers that are not in your deck."),
 "am": dict(
   scenario="You are an <b>analyst in Asset Management</b>. The CIO needs the Q3 review of the <b>Gulf Opportunities Fund</b> for the fund board — and the call has moved to tomorrow morning.",
   xlsx=("kgof-q3-fund-pack.xlsx", "Fund pack — Monthly_Returns, Holdings_30Sep, Flows, Policy"),
   clean=["In Monthly_Returns, make every return a number — one of them is stored as text. Tell me which one you fixed.",
          "In Holdings_30Sep, find any holding that appears twice and remove the duplicate. Check the weights at 30 Sep add up to about 100%.",
          "In Flows, trim spaces and make the Channel labels consistent (Institutional or Retail), and convert any number stored as text. Add a column Net flow = Subscriptions − Redemptions."],
   analyse=["Add columns for cumulative fund return and cumulative benchmark return since January, compounding the monthly returns: (1 + return) multiplied month by month, minus 1. Give me the year-to-date and Q3 (Jul–Sep) figures for both, and the difference.",
            "Add a column Excess = Fund − Benchmark for each month. Which month was best and which was worst against the benchmark?",
            "Sum Weight 30-Sep % by Sector and compare with the Policy sheet: any sector above 35%, any single stock above 10%, and is cash inside 2–10%? Then add Contribution = Weight 30-Jun % × Q3 return % ÷ 100 and show the top 3 and bottom 3.",
            "Sum Net flow by month and give me year-to-date and Q3 totals."],
   findings=[("YTD return: fund vs benchmark", "one decimal place"), ("Q3 return: fund vs benchmark", ""), ("Fund rule breaches", "sector · single stock"), ("Top and bottom contributor in Q3", ""), ("Net flows YTD and Q3 (KWD '000)", "")],
   chart="Create a line chart of cumulative fund return and cumulative benchmark return from January to September. Add a column chart of net flow by month. Give each chart a title that says the message.",
   brief_to="Dalal Al-Sabah, Chief Investment Officer (internal)",
   deck_for="the fund board (lead with whether the fund is inside its rules; every return to one decimal place)",
   brief_sections="Bottom line · Performance table (YTD and Q3, fund vs benchmark) · Rule check (sector, single stock, cash) · Contributors · Flows · Actions",
   deck_slides="1 The message in one line · 2 Performance vs benchmark (your line chart) · 3 Inside the rules? · 4 What drove Q3 · 5 Flows (your column chart) · 6 Actions for the board",
   decline="Bader asked for a line saying the fund will beat the benchmark in Q4. Your reply must decline it — the fund rules never allow promising future returns.",
   stretch="Ask Copilot: <i>“What would the fund's sector weights be if we cut Banks to 34% and moved the difference to cash?”</i> Is cash still inside 10%?",
   boss="Ask Copilot to explain, in two sentences a board member would understand, why the fund beat the benchmark in Q3. Check that every reason is supported by your contributors table."),
 "ops": dict(
   scenario="You are an <b>Operations analyst</b>. The COO needs the Q3 settlement review for the Operations Committee — tomorrow at 8:30. The blotter export is messy and some trades are still open.",
   xlsx=("ops-q3-settlement-blotter.xlsx", "Settlement blotter — Trades_Q3, Policy"),
   clean=["Highlight duplicate rows based on Trade ID. Remove them and tell me how many trades are left.",
          "Add a column Counterparty (clean) that maps every spelling to one name — for example GULF BROKERAGE CO and Gulf Brokerage both become Gulf Brokerage Co.",
          "Make every value in Actual settle a real date — some are stored as text. Leave the open fails blank."],
   analyse=["Add a column Days late = Actual settle − Expected settle (calendar days). For trades with no Actual settle, add Days open = 30 Sep 2026 − Expected settle.",
            "Count trades by Status. What % settled on time? Compare with the 98% target in the Policy sheet.",
            "Create a PivotTable of late and failed trades by Counterparty (clean), with their total Value KWD. Which counterparties have 3 or more?",
            "List every open fail with Days open above 5 — Trade ID, counterparty, days open and value. Then show the on-time rate by month (Jul, Aug, Sep)."],
   findings=[("Unique trades and on-time %", ""), ("Late trades: count, value and average days late", ""), ("Trades to escalate", "Trade IDs"), ("Counterparties for review", "3 or more"), ("Best and worst month", "on-time %")],
   chart="Create a bar chart of late and failed trades by counterparty, and a line chart of the on-time rate by month with the 98% target as a second line. Give each chart a title that says the message.",
   brief_to="Mishari Al-Ghanim, Chief Operating Officer",
   deck_for="the Operations Committee (trade IDs and counterparties only — no client names)",
   brief_sections="Bottom line: did we meet 98%? · Key numbers table · Escalations (open fails > 5 days) · Counterparty review · Root causes to check · Actions before Q4",
   deck_slides="1 The message in one line · 2 On-time rate vs target (your line chart) · 3 Where the fails come from (your bar chart) · 4 Escalate today · 5 Counterparty review · 6 Actions before Q4",
   decline="Riyadh Capital Markets asked for KAMCO's internal counterparty scores. Your reply must confirm you will not share them outside KAMCO.",
   stretch="Ask Copilot: <i>“If the three open fails had settled on time, what would the on-time rate be?”</i> Check it by hand.",
   boss="Draft a short, firm email to the counterparty with the most late trades asking for a root-cause note by Thursday. No internal scores, no client names."),
 "rs": dict(
   scenario="You are an <b>Investment Research analyst</b>. The Head of Research wants your initiation view on <b>Wafra Logistics Co.</b> for the Investment Committee — tomorrow morning, not Thursday.",
   xlsx=("wafra-logistics-research-pack.xlsx", "Research pack — Financials, Peers, Share_Price, Policy"),
   clean=["In Financials, make every number a real number — one is stored as text with a comma. Tell me which one.",
          "In Peers, remove any peer listed twice and mark any peer without an EV/EBITDA number as excluded. How many peers are left with a number?",
          "Turn the Share_Price month labels into real dates so we can chart them."],
   analyse=["Add EBITDA margin = EBITDA ÷ Revenue for each column, and revenue growth year on year. Give me the revenue CAGR from FY2023 to FY2025. Remind me that H1 2026 is six months only.",
            "Calculate net debt = Total debt − Cash for FY2025, and net debt ÷ EBITDA.",
            "Following the Policy sheet exactly: peer median EV/EBITDA (each peer once, excluding n/a) × FY2025 EBITDA = EV; EV − net debt = equity value; ÷ shares = value per share; ÷ the 30 Sep price − 1 = upside. Show each step and which view it gives: Attractive, Neutral or Unattractive."],
   findings=[("Revenue CAGR FY2023–FY2025", ""), ("EBITDA margin FY2025", ""), ("Net debt / EBITDA FY2025", ""), ("Peer median EV/EBITDA", "x"), ("Value per share vs price — upside — view", "")],
   chart="Create a combo chart: revenue as columns and EBITDA margin as a line, FY2023 to FY2025. Then a line chart of the month-end share price. Give each chart a title that says the message.",
   brief_to="Ahmad Al-Hamad, Head of Research (internal — Investment Committee use only)",
   deck_for="the Investment Committee (no price targets or promises; the valuation table on one slide)",
   brief_sections="Bottom line: the view in one line · Business in numbers (growth, margins, leverage) · Valuation table (every step) · What the market already prices in · What would change the view",
   deck_slides="1 The view in one line · 2 Growth and margins (your combo chart) · 3 Balance sheet and leverage · 4 Valuation vs peers · 5 The share price (your line chart) · 6 Risks and what would change the view",
   decline="Sara in Corporate Finance asked for the valuation before the Committee, to pass to a client. Your reply must say research cannot be shared before the Committee — and never with a client.",
   stretch="Ask Copilot: <i>“At what EV/EBITDA multiple would the value per share equal today's price?”</i> Check it by hand — it tells the Committee what the market is already assuming.",
   boss="Ask Copilot for the strongest argument <b>against</b> your view. Add one line to your brief that answers it."),
}

SPEC["fin"] = dict(
   scenario="You are a <b>Finance analyst</b>. The CFO needs the Q3 budget vs actual review for the Management Committee — tomorrow at 8:00. One department head is asking you to move costs between quarters.",
   xlsx=("fin-q3-budget-vs-actual.xlsx", "Ledger export and budget — Actuals_Q3, Budget_Q3, Policy"),
   clean=["Highlight duplicate rows in Actuals_Q3 based on Reference. Remove them and tell me how many lines are left.",
          "Add a column Department (clean) that maps every spelling to one name — for example Wealth Mgmt and WEALTH MANAGEMENT both become Wealth Management; Ops becomes Operations; Information Technology becomes IT.",
          "Make every value in Amount KWD a real number — some are stored as text with a comma."],
   analyse=["Create a PivotTable of Amount KWD by Department (clean). Next to it, bring in the budget for each department from Budget_Q3 (sum of its categories). Add Variance KWD = Actual − Budget and Variance % = Actual ÷ Budget − 1.",
            "Following the Policy sheet, which departments are more than 10% AND more than KWD 5,000 over budget?",
            "Show the top 3 vendors by total spend, and total spend by month (Jul, Aug, Sep)."],
   findings=[("Total actual vs budget (KWD and %)", ""), ("Most over budget — department and %", ""), ("Departments that must explain", ""), ("Top vendor", ""), ("Highest spending month", "")],
   chart="Create a clustered column chart of budget vs actual by department, and a line chart of monthly spend. Give each chart a title that says the message, for example “IT and Wealth Management drove the overspend”.",
   brief_to="Reem Al-Fulaij, Chief Financial Officer",
   deck_for="the Management Committee (lead with the total variance; name the departments that must explain)",
   brief_sections="Bottom line: total variance in one line · Budget vs actual table by department · Who must explain, and why · Where the money went (top vendors, monthly trend) · Actions for Q4",
   deck_slides="1 The message in one line · 2 Total budget vs actual · 3 By department (your column chart) · 4 Who must explain · 5 Spend over the quarter (your line chart) · 6 Actions for Q4",
   decline="Talal asked Finance to move KWD 20,000 of September costs into Q4. Your reply must decline: costs stay in the quarter they were incurred.",
   stretch="Ask Copilot: <i>“If IT's early licence renewals of about KWD 20,000 are a timing difference, what would IT's variance be without them?”</i> Present it as a note, not as a change to the numbers.",
   boss="Draft the two-line question the CFO should ask each department that must explain. Make it neutral — no blame.")
SPEC["hr"] = dict(
   scenario="You are an <b>HR analyst</b>. The HR Director needs the Q3 people review for the Management Committee — tomorrow at 9:00. A manager wants something the survey rules don't allow.",
   xlsx=("hr-q3-people-pack.xlsx", "People pack — Headcount_Q3, Engagement_Q3, Policy"),
   clean=["Highlight duplicate rows in Headcount_Q3 based on Employee ID. Remove them and tell me how many employees are left.",
          "Add a column Department (clean) that maps every spelling to one name — Ops becomes Operations, Wealth Mgmt becomes Wealth Management, HR and Admin becomes HR & Admin.",
          "Make every value in Leave date a real date — some are stored as text. Leave it blank for people who have not left."],
   analyse=["How many employees were there at the start of Q3, how many left in Q3, and what is the attrition rate (leavers ÷ headcount at the start, as in the Policy sheet)? Then show the same by Department (clean).",
            "Count leavers by Exit reason and show the top 3.",
            "Average Training hours Q3 by department, compared with the 10-hour target. Which departments are below target?",
            "From Engagement_Q3, which department has the lowest engagement score? Put attrition, training and engagement side by side by department."],
   findings=[("Headcount, leavers and attrition %", ""), ("Department with the highest attrition", ""), ("Top exit reason", ""), ("Departments below the training target", ""), ("Lowest engagement", "")],
   chart="Create a bar chart of attrition % by department, and a bar chart of engagement score by department. Give each chart a title that says the message.",
   brief_to="Abeer Al-Khaled, HR Director",
   deck_for="the Management Committee (employee IDs only — no names; survey results at department level only)",
   brief_sections="Bottom line: attrition in one line · People numbers by department · Why people leave · Training vs target · Engagement · The department to act on first, and how",
   deck_slides="1 The message in one line · 2 Attrition by department (your chart) · 3 Why people leave · 4 Training vs target · 5 Engagement (your chart) · 6 Where to act first",
   decline="Nasser asked for named individual survey answers. Your reply must decline: the survey is anonymous. Offer department-level results and an action plan instead.",
   stretch="Ask Copilot: <i>“Which department has the same pattern as Operations on two of the three measures?”</i> Add one line to the brief if it matters.",
   boss="Draft a short note to Nasser that declines the named answers kindly and proposes three practical next steps for his team.")
SPEC["lc"] = dict(
   scenario="You are a <b>Compliance analyst</b>. The Chief Compliance Officer needs the Q3 complaints review for the Board Audit & Risk Committee — tomorrow at 8:30. Sales wants client details it should not have.",
   xlsx=("lc-q3-complaints-log.xlsx", "Complaints log — Complaints_Q3, Policy"),
   clean=["Highlight duplicate rows based on Complaint ID. Remove them and tell me how many complaints are left.",
          "Add a column Category (clean) that maps every label to one of: Statement delay, Fees & charges, Advice suitability, Service & communication, Transfer delay.",
          "Make every value in Date acknowledged a real date — some are stored as text in dd/mm/yyyy."],
   analyse=["Count complaints by Category (clean) and by Channel.",
            "Add a column Business days to acknowledge (Friday and Saturday are closed). What % were acknowledged within 2 business days?",
            "For closed complaints, add Days to resolve = Date resolved − Date received. What % were resolved within 15 days? Then list every open complaint received more than 15 days before 30 Sep 2026 — ID, category and days open.",
            "Total compensation paid on closed complaints."],
   findings=[("Complaints in Q3 and the largest category", ""), ("% acknowledged within 2 business days", ""), ("% of closed resolved within 15 days", ""), ("Overdue open complaints (IDs)", ""), ("Compensation paid (KWD)", "")],
   chart="Create a bar chart of complaints by category, and a chart comparing the two on-time rates with the standard. Give each chart a title that says the message.",
   brief_to="Hanan Al-Sabah, Chief Compliance Officer",
   deck_for="the Board Audit & Risk Committee (complaint IDs only — never client details)",
   brief_sections="Bottom line: do we meet the standard? · Complaints by category and channel · Acknowledge and resolve rates · Overdue complaints (IDs) · Root causes · Actions",
   deck_slides="1 The message in one line · 2 What clients complain about (your chart) · 3 Are we on time? (your chart) · 4 Overdue — escalate now · 5 Root causes · 6 Actions",
   decline="Fawaz asked for the names and phone numbers of clients who complained about fees, for a sales call. Your reply must decline: client details stay inside Compliance.",
   stretch="Ask Copilot: <i>“Which category takes longest to resolve on average?”</i> Is it the same as the largest category?",
   boss="Write the one-paragraph root-cause note the Committee will ask for on statement delays — what you know from the data, and what you would still need to find out.")


def capstone_task(cap):
    roles = {}
    for k, sp in SPEC.items():
        th = cap["threads"][k]
        steps = [
         {"label": "1 · Summarise the request · Outlook · 10 min",
          "goal": "Get the real ask from the thread: the <b>final</b> deadline, the two files and their format, who each one is for, the rules you must follow — and the request you must decline. The newest message wins.",
          "prompt": "Summarise this thread. List the final deadline, each file I must send with its format and audience, the rules I must follow, and any request I should decline and why. Use the newest message when instructions change.",
          "findings": [{"label": "Final deadline", "hint": ""}, {"label": "File 1 and file 2 — format and audience", "hint": ""}, {"label": "The request you will decline — and why", "hint": ""}]},
         {"label": "2 · Clean the data · Excel · 15 min",
          "goal": "Save the workbook to OneDrive, open it in Excel, delete the title rows above each header and press <b>Ctrl+T</b>. Then clean it with Copilot — check the row count before and after every step. Suggested prompts, in order: " + " ".join(f"<br>• <i>{p}</i>" for p in sp["clean"]),
          "prompt": sp["clean"][0],
          "findings": [{"label": "Rows before → after cleaning", "hint": ""}, {"label": "Every problem you found and fixed", "hint": ""}]},
         {"label": "3 · Analyse · Excel · 18 min",
          "goal": "Answer every question in the email with numbers you can trace. Ask Copilot to <b>show the formula</b>, and test one row by hand. Suggested prompts: " + " ".join(f"<br>• <i>{p}</i>" for p in sp["analyse"]),
          "prompt": sp["analyse"][0],
          "findings": [{"label": l, "hint": h} for l, h in sp["findings"]]},
         {"label": "4 · Chart it · Excel · 8 min",
          "goal": sp["chart"] + " Check the chart against your table — axis, labels, units.",
          "prompt": sp["chart"],
          "findings": [{"label": "Your chart title(s) — the message", "hint": ""}]},
         {"label": "5 · Executive brief · Word · 18 min",
          "goal": f"A <b>one-page</b> executive brief for {sp['brief_to']}. Sections: {sp['brief_sections']}. Draft it from your own checked numbers — paste them in — then ground it in the house view with <kbd>/</kbd> for the number format. Paste your chart from Excel.",
          "prompt": "Using the numbers below, draft a one-page executive brief for [reader]. Start with a two-line bottom line. Then: a key numbers table, the findings, a recommendation, and next steps. Under 350 words. Plain English, no jargon. Show KWD without decimals and percentages to one decimal place, as in /house-view-q4-2026. [paste your numbers]",
          "findings": [{"label": "Your bottom line — two lines", "hint": ""}]},
         {"label": "6 · PowerPoint · 18 min",
          "goal": f"A <b>6-slide deck</b> for {sp['deck_for']}. In PowerPoint, select <b>Create a presentation from a file</b> and point it at your brief. Slides: {sp['deck_slides']}. Every title is the message. Paste your chart(s) from Excel.",
          "prompt": "Create a 6-slide presentation from /[your executive brief]. Make every slide title the message, not the topic. Keep every number exactly as in the brief. Add speaker notes. [Client-facing? Add the standard disclaimer from /house-view-q4-2026 on the last slide.]",
          "findings": [{"label": "One number you checked on a slide against Excel", "hint": ""}]},
         {"label": "7 · Check and reply · Outlook · 13 min",
          "goal": f"Run the four checks before you send — <b>accuracy</b> (every number in the brief and the deck matches Excel), <b>confidentiality</b>, <b>tone</b>, <b>completeness</b>. {sp['decline']} Then send your reply to <b>aya@joincoded.com</b> with <b>both files attached</b>, matching the tone of the request. Run <b>Coaching by Copilot</b>. End with one line: <b>“What I corrected: …”</b> — what Copilot got wrong and you fixed — and paste <b>your three best prompts</b> underneath.",
          "prompt": "Draft my reply. Say the executive brief and the deck are attached, give the bottom line in one sentence, and politely decline [the request] with a one-line reason. Under 120 words. Professional and warm.",
          "findings": [{"label": "What I corrected", "hint": "the line that ends your reply"}]},
        ]
        roles[k] = dict(
            scenario=sp["scenario"] + " <b>Pick your field above.</b> Everything you need is on this page: the email thread, the workbook and the house view.",
            briefs=[{"label": "Email thread · " + th["subject"], "text": th["text"]}],
            files=[{"label": sp["xlsx"][0] + " · " + sp["xlsx"][1], "href": sp["xlsx"][0], "note": "<b>Your data.</b> Save it to your <b>OneDrive</b> first — Copilot in Excel needs AutoSave on."},
                   {"label": f"capstone-{k}-request.eml · the same thread as an email, with the workbook attached", "href": f"capstone-{k}-request.eml",
                    "note": "Optional: open it in Outlook desktop to use Summary by Copilot on a real email."}, HV],
            promptSteps=steps,
            stretch=sp["stretch"], boss=sp["boss"])
    return dict(
        id="E2.9", app="Capstone", title="Capstone — your field, start to finish", minutes="13:10 – 14:50 · 100 min", block="Capstone · graded",
        scenario="", roles=roles,
        steps=["<b>Pick your field</b> with the buttons above — seven desks, from Wealth Management to Human Resources.",
               "Work <b>alone</b>, in order, through the seven steps below. Help from Copilot is the point — help from neighbours is not.",
               "Each step has a goal. Write your own CTFT prompt first; tap <b>Reveal a suggested prompt</b> only if you are stuck.",
               "By <b>2:50 pm</b>, email your final reply to <b>aya@joincoded.com</b> with the subject <b>Capstone · [your field] · [your name]</b> and <b>both files attached</b>: the executive brief (Word) and the deck (PowerPoint).",
               "At <b>2:50 pm</b>, present your workflow to a partner — <b>2 minutes</b>: the request, one number and one chart, and what you corrected."],
        expect="Scored out of 100 — pass or does not pass: <b>30</b> workflow completeness (all seven steps, reply sent by 2:50 pm) · <b>25</b> data analysis accuracy (no major errors) · <b>20</b> deliverable quality (brief, deck and charts answer the request) · <b>15</b> AI review &amp; judgement (accuracy, confidentiality, tone, completeness — your “What I corrected” line) · <b>10</b> prompt quality (your three best prompts).")


def patch_roles(html):
    old = "var ROLES = { executive: 'Executive', sales: 'Sales', marketing: 'Marketing', technical: 'Technical' };"
    assert old in html
    html = html.replace(old, "var ROLES = " + json.dumps(FIELDS) + ";")
    for a, b in [('<span class="rt-k">Scenario for:</span>', '<span class="rt-k">Your field:</span>'),
                 ("Pick your track — the lab remembers it.", "Pick your field — the lab remembers it."),
                 ("Showing your track. Tap another to switch.", "Showing your field. Tap another to switch.")]:
        assert a in html, a
        html = html.replace(a, b)
    return html
