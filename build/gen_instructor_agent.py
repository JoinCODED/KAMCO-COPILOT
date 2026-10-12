"""Instructor demo agent: HR & Employee Onboarding Assistant — three knowledge files + a facilitator demo page."""
import os, html as H
from docx import Document
from docx.shared import Pt
from email.message import EmailMessage

FILES = "out/files"; FAC = "out/facilitator"
NOTE = "TRAINING SAMPLE — fictional KAMCO policy for the AI at Work with Microsoft Copilot program. Not legal advice."


def doc(fn, title, secs, table=None):
    d = Document(); d.styles["Normal"].font.name = "Arial"; d.styles["Normal"].font.size = Pt(10.5)
    d.add_heading(title, 0)
    p = d.add_paragraph(NOTE); p.runs[0].italic = True
    for h, bullets in secs:
        d.add_heading(h, 1)
        for b in bullets:
            d.add_paragraph(b, style="List Bullet")
    if table:
        d.add_heading(table[0], 1)
        t = d.add_table(rows=1, cols=len(table[1])); t.style = "Light Grid Accent 1"
        for c, h in zip(t.rows[0].cells, table[1]):
            c.text = h
        for r in table[2]:
            for c, v in zip(t.add_row().cells, r):
                c.text = v
        if len(table) > 3:
            for b in table[3]:
                d.add_paragraph(b, style="List Bullet")
    d.save(os.path.join(FILES, fn))


doc("demo-employee-handbook-2026.docx", "KAMCO Employee Handbook 2026 (training)", [
  ("1. Working hours", ["Sunday to Thursday, 8:00 to 16:00. Friday and Saturday are the weekend.", "During Ramadan: 9:00 to 14:00."]),
  ("2. Probation", ["Probation is 100 working days from the start date.", "Your manager holds check-ins at 30, 60 and 90 days."]),
  ("3. Before day 1 — documents to bring", ["Civil ID (copy of both sides).", "Passport (copy).", "Bank letter showing your IBAN, for salary.",
                                           "Educational certificates (copies).", "One passport-size photo, for your access badge."]),
  ("4. Day 1", ["9:00 — welcome at HR: contract, badge and photo.", "10:30 — IT: laptop, KAMCO account and Microsoft 365 Copilot set-up.",
                "12:00 — lunch with your manager and your onboarding buddy.", "14:00 — tour of the office and your team's systems."]),
  ("5. First week", ["Complete the Code of Conduct and Compliance training by day 5.", "Meet your onboarding buddy every day for 15 minutes.",
                     "Agree your 90-day goals with your manager by day 5."]),
  ("6. Annual leave", ["30 days of paid annual leave a year.", "You can take your first annual leave after 9 months of service.",
                       "Apply in the HR system at least 2 weeks before the leave starts."]),
  ("7. Sick leave", ["Tell your manager before 9:00 on the first day.", "A medical certificate is needed for any absence longer than 1 day."]),
  ("8. Hybrid work", ["After probation, up to 2 remote days a week with your manager's approval. Not during probation."]),
  ("9. Privacy", ["HR never shares one employee's salary, personal data or records with another employee.",
                  "Questions not covered here: hr@kamco-training.example."])])
doc("demo-benefits-guide-2026.docx", "KAMCO Employee Benefits Guide 2026 (training)", [
  ("1. Medical insurance", ["Starts on day 1 for the employee, spouse and up to 3 children under 21.", "Add family members within 30 days of joining — after that, at the next renewal only."]),
  ("2. Allowances (monthly)", ["Transport: KWD 50.", "Mobile phone: KWD 15.", "Gym: KWD 20, with a receipt."]),
  ("3. Learning", ["Training budget: KWD 600 a year, approved by your manager.", "Professional certificates (CFA, CIPM, ACCA): exam fees paid once you pass."]),
  ("4. Special leave", ["Marriage: 3 working days.", "New baby — father: 3 working days.", "Maternity: 70 days on full pay.",
                        "Hajj: 21 days on full pay, once during your service, after 2 years."]),
  ("5. Staff investing", ["50% discount on management fees for KAMCO funds."]),
  ("6. Questions", ["Benefits not covered here: hr@kamco-training.example."])])
HOL = [("New Year's Day", "Thursday 1 January", "Fixed"),
       ("Isra and Mi'raj", "Friday 16 January", "Expected — moon sighting"),
       ("National Day", "Wednesday 25 February", "Fixed"),
       ("Liberation Day", "Thursday 26 February", "Fixed"),
       ("Eid al-Fitr", "Friday 20 March to Sunday 22 March", "Expected — moon sighting"),
       ("Arafat Day", "Tuesday 26 May", "Expected — moon sighting"),
       ("Eid al-Adha", "Wednesday 27 May to Friday 29 May", "Expected — moon sighting"),
       ("Islamic New Year", "Tuesday 16 June", "Expected — moon sighting"),
       ("Prophet's Birthday", "Wednesday 26 August", "Expected — moon sighting")]
doc("demo-kuwait-public-holidays-2026.docx", "Kuwait Public Holidays 2026 (training reference)", [
  ("How to use this calendar", ["KAMCO follows the official public holidays announced by the Civil Service Commission.",
                                "Islamic holidays depend on moon sighting. The dates below are the expected dates — the official dates and any extra bridge days are announced shortly before each holiday.",
                                "If a holiday falls on a Friday or Saturday, follow the official announcement for any compensation day."])],
    table=("2026 public holidays", ["Holiday", "Date (2026)", "Status"], HOL,
           ["The next fixed public holiday after these is New Year's Day, Friday 1 January 2027."]))
REQ = """From: Abeer Al-Khaled (HR Director)
Sent: Mon 12 Oct 2026, 10:05
To: You

Hi,

Sara Al-Ali joins Wealth Management as an Associate on Sunday 15 November 2026. Her manager is Faisal Al-Mutairi.

Please prepare her onboarding plan: what she must bring, her first day, her first week, and the benefits she needs to set up. She has a husband and two children who need medical cover.

She has already asked if she can take a week off in January to travel. What do I tell her?

Thanks,
Abeer"""
m = EmailMessage(); m["Subject"] = "New joiner - Sara Al-Ali, Wealth Management, starts 15 Nov"; m["From"] = "Abeer Al-Khaled"; m["To"] = "you@kamco-training.example"
m.set_content(REQ); open(os.path.join(FILES, "demo-onboarding-request.eml"), "wb").write(bytes(m))
open(os.path.join(FILES, "demo-onboarding-request.txt"), "w").write(REQ)

NAME = "HR & Employee Onboarding Assistant"
DESC = "Helps KAMCO HR staff and managers onboard new employees and answers staff questions on policies, benefits and public holidays — from the HR files only."
INSTR = ("You help KAMCO HR staff and managers onboard new employees and answer employee questions.\n"
         "Use only the three files: the Employee Handbook 2026, the Benefits Guide 2026 and the Kuwait Public Holidays 2026 calendar.\n"
         "For a new joiner, give: 1) documents to bring; 2) the day 1 plan; 3) the first-week plan; 4) benefits to set up, with any deadlines; 5) key dates.\n"
         "For a question: the short answer first, then the rule and the file it came from. Show any calculation step by step.\n"
         "Friday and Saturday are the weekend. For Islamic holidays, say the date is expected and confirmed by the official announcement.\n"
         "Never share or guess any employee's salary or personal data.\n"
         "If the answer is not in the files, say so and suggest emailing hr@kamco-training.example. Do not guess.")
PROMPTS = [("Plan a new joiner", "Prepare the onboarding plan for this new joiner: [paste the email]"),
           ("Public holidays", "Which public holidays are left in 2026, and which fall on a working day?")]
TESTS = [("1 · The new joiner", "Paste Abeer's email (below) and send: <i>Prepare the onboarding plan for this new joiner.</i>",
          "Documents (Civil ID, passport, IBAN letter, certificates, photo) · Day 1 timetable · first week (Compliance training and 90-day goals by day 5, daily buddy check-in) · medical for husband and 2 children — <b>add them within 30 days</b> · transport and mobile allowances · <b>no annual leave in January</b> (first leave after 9 months)."),
         ("2 · The calendar", "<i>How many working days does the Arafat Day and Eid al-Adha holiday cover in 2026?</i>",
          "Tue 26 to Fri 29 May (expected) → 3 working days: 26, 27 and 28 May. Friday 29 May is already the weekend. It should say the dates are expected, pending the official announcement."),
         ("3 · Maths", "<i>What will Sara receive in transport and mobile allowances in her first full year?</i>",
          "(KWD 50 + KWD 15) × 12 = KWD 780."),
         ("4 · Not in the files — and private", "<i>What salary will Sara get?</i>",
          "Says salaries are not in the files and it never shares an employee's pay — suggests hr@kamco-training.example.")]

css = """:root{--bg:#00112F;--card:#0b2147;--line:#1d3a6b;--ink:#eef3ff;--dim:#a9b8d6;--blue:#4a87e8;--amber:#eab94a;--green:#5fd39a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 Inter,system-ui,sans-serif}
main{max-width:980px;margin:0 auto;padding:32px 20px 60px}h1{font-size:30px;margin:0 0 6px}h2{font-size:21px;margin:30px 0 10px;color:var(--blue)}
.sub{color:var(--dim)}.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px 20px;margin:12px 0}
.k{font:600 12px/1 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);margin-bottom:8px}
pre{white-space:pre-wrap;background:#06183a;border:1px solid var(--line);border-radius:10px;padding:12px;font:13.5px/1.55 ui-monospace,monospace;color:#d8e3ff;cursor:pointer;position:relative}
pre:hover{border-color:var(--blue)}pre.ok{border-color:var(--green)}
a{color:var(--blue)}table{width:100%;border-collapse:collapse}td{border-top:1px solid var(--line);padding:9px 6px;vertical-align:top}td:first-child{width:24%;color:var(--dim)}
.say{border-left:3px solid var(--amber);padding:8px 14px;margin:10px 0;color:#f3e3bd;background:rgba(234,185,74,.06)}ol li{margin:6px 0}
.dl a{display:inline-block;margin:4px 10px 4px 0;padding:8px 12px;border:1px solid var(--line);border-radius:10px;text-decoration:none}"""
pre = lambda t: f"<pre title='Click to copy' onclick=\"navigator.clipboard.writeText(this.innerText);this.classList.add('ok')\">{H.escape(t)}</pre>"
out = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Instructor agent demo — KAMCO Copilot</title><style>{css}</style></head><body><main>",
 "<h1>Instructor demo · HR &amp; Employee Onboarding Assistant</h1>",
 "<p class='sub'>Day 2, Block 3 — run it on screen just before trainees build their own agent (E2.8). About 8 minutes. Trainees build a different agent for their own field, so they can't just copy yours. Click any grey box to copy it.</p>",
 "<h2>Before the session (2 min)</h2><div class='card'><ol>"
 "<li>Save the three .docx files to your OneDrive. Keep Abeer's email open to copy.</li>"
 "<li>Microsoft 365 Copilot app → <b>Create agent</b> (or <b>New agent</b>) → <b>Configure</b>.</li></ol>"
 "<div class='dl'><a href='demo-employee-handbook-2026.docx' download>⬇ demo-employee-handbook-2026.docx</a><a href='demo-benefits-guide-2026.docx' download>⬇ demo-benefits-guide-2026.docx</a><a href='demo-kuwait-public-holidays-2026.docx' download>⬇ demo-kuwait-public-holidays-2026.docx</a><a href='demo-onboarding-request.txt' download>⬇ demo-onboarding-request.txt</a><a href='demo-onboarding-request.eml' download>⬇ demo-onboarding-request.eml</a></div></div>",
 "<div class='say'>“Every new joiner — and every manager — asks HR the same questions: what do I bring, what happens on day one, when can I take leave, what's covered? Same answers, every time. That's a job for an agent.”</div>",
 "<h2>Build it (3 min)</h2>",
 "<div class='card'><div class='k'>1 · Name</div>" + pre(NAME) + "<div class='k'>2 · Description</div>" + pre(DESC) + "<div class='k'>3 · Instructions</div>" + pre(INSTR) +
 "<p>Point at the CTFT: <b>Context</b> (who it helps, which files) · <b>Task</b> (the five parts of an onboarding plan) · <b>Format</b> (short answer, then the rule and the file) · <b>Limits</b> (never share pay or personal data; don't guess).</p>"
 "<div class='k'>4 · Knowledge</div><p>Add the three files: <b>demo-employee-handbook-2026.docx</b>, <b>demo-benefits-guide-2026.docx</b>, <b>demo-kuwait-public-holidays-2026.docx</b>. Turn <b>Web search off</b>.</p>"
 "<div class='k'>5 · Suggested prompts</div>" + "".join(f"<p><b>{H.escape(t)}</b></p>" + pre(m_) for t, m_ in PROMPTS) + "</div>",
 "<h2>Test it (5 min) — in Preview, then Create</h2><div class='card'><table>" +
 "".join(f"<tr><td><b>{a}</b><br>{b}</td><td>{c}</td></tr>" for a, b, c in TESTS) + "</table>"
 "<p style='margin-top:12px'>Test 1 — Abeer's email:</p>" + pre(REQ) +
 "<div class='say'>“It caught the 30-day deadline for family medical cover, it said no to January leave — with the reason — and it refused to guess a salary. That's the instructions working. Now — Create. It stays private until I share it.”</div></div>",
 "<h2>The points to land</h2><div class='card'><ol><li><b>Instructions are a prompt that never goes away</b> — CTFT, written once.</li>"
 "<li><b>Knowledge is what it reads</b> — and nothing else, once web search is off.</li>"
 "<li><b>Test before you trust</b> — a real request, a shortcut, a date, a gap.</li>"
 "<li><b>Share the agent = share the files.</b> Anyone who chats with it gets answers from your uploads.</li></ol></div>",
 "<h2>If something goes wrong</h2><div class='card'><table>"
 "<tr><td>No Create agent button</td><td>Agent Builder may be switched off by IT. Run it in Copilot Chat: paste the instructions, upload the three files with +, run the tests. Same lesson.</td></tr>"
 ""
 "<tr><td>It guesses a salary</td><td>Check Web search is off. Add: <i>“If the answer is not in the files, say so — never estimate.”</i> Retest.</td></tr>"
 "<tr><td>Date maths is off by a day</td><td>Say: “Maths and dates are a known blind spot — this is why we check.” Then show the count on screen.</td></tr></table></div>",
 "</main></body></html>"]
open(os.path.join(FAC, "instructor-agent-demo.html"), "w", encoding="utf-8").write("\n".join(out))
for fn in ["demo-employee-handbook-2026.docx", "demo-benefits-guide-2026.docx", "demo-kuwait-public-holidays-2026.docx", "demo-onboarding-request.eml", "demo-onboarding-request.txt"]:
    import shutil; shutil.copy(os.path.join(FILES, fn), FAC)
print("instructor agent demo")
