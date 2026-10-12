"""Instructor demo agent: Client Onboarding Assistant — files + a facilitator demo page."""
import os, html as H
from docx import Document
from docx.shared import Pt
from email.message import EmailMessage

FILES = "out/files"; FAC = "out/facilitator"


def doc(fn, title, secs):
    d = Document(); d.styles["Normal"].font.name = "Arial"; d.styles["Normal"].font.size = Pt(10.5)
    d.add_heading(title, 0)
    p = d.add_paragraph("TRAINING SAMPLE — fictional content for the AI at Work with Microsoft Copilot program."); p.runs[0].italic = True
    for h, bullets in secs:
        d.add_heading(h, 1)
        for b in bullets:
            d.add_paragraph(b, style="List Bullet")
    d.save(os.path.join(FILES, fn))


doc("demo-onboarding-checklist-2026.docx", "KAMCO Client Onboarding Checklist 2026 (training)", [
  ("1. Who this covers", ["New wealth management clients: individuals and companies opening a discretionary portfolio."]),
  ("2. Minimum investment", ["KWD 100,000 for a discretionary portfolio. (This replaces the 2024 guide, which said KWD 50,000.)"]),
  ("3. Documents — individuals", ["Civil ID (valid).", "Proof of address dated within the last 3 months.", "Source of funds declaration, signed.", "Signed risk profile questionnaire."]),
  ("4. Documents — companies", ["Commercial licence (valid).", "Articles of association.", "Authorised signatories list with their Civil IDs.",
                                "Ultimate beneficial owners: everyone who owns 25% or more.", "Latest audited financial statements.", "Signed risk profile questionnaire."]),
  ("5. Approvals and timing", ["Compliance must approve KYC before any account is opened or any money is accepted — no exceptions, for any client.",
                               "Politically exposed persons (PEPs) also need the Chief Compliance Officer's approval.",
                               "Target: onboarding complete within 10 business days of receiving all documents. Friday and Saturday are not business days."]),
  ("6. Contacts", ["Questions not covered here: onboarding@kamco-training.example."])])
doc("demo-onboarding-guide-2024.docx", "KAMCO Onboarding Guide 2024 (training) — older version", [
  ("Minimum investment", ["KWD 50,000 for a discretionary portfolio."]),
  ("Proof of address", ["Must be dated within the last 6 months."]),
  ("Timing", ["Aim to complete onboarding within 15 business days."])])
REQ = """From: Yousef Al-Kandari (Senior Relationship Manager)
Sent: Mon 12 Oct 2026, 09:20
To: You

Hi,

Good news - Al-Fanar Trading Co. wants to open a discretionary portfolio with us. They plan to start with KWD 75,000 and add more next year.

The owners are two brothers (60% and 30%) and a cousin with 10%. Their CFO sent the commercial licence and last year's audited accounts. They want the account open by Thursday so they can transfer the money this week - can we start investing before KYC is finished, since they are a well-known family?

What else do we need from them, and is Thursday realistic?

Thanks,
Yousef"""
m = EmailMessage(); m["Subject"] = "New client - Al-Fanar Trading Co. (corporate) - what do we need?"; m["From"] = "Yousef Al-Kandari"; m["To"] = "you@kamco-training.example"
m.set_content(REQ); open(os.path.join(FILES, "demo-onboarding-request.eml"), "wb").write(bytes(m))
open(os.path.join(FILES, "demo-onboarding-request.txt"), "w").write(REQ)

NAME = "Client Onboarding Assistant"
DESC = "Answers KAMCO staff questions about onboarding new wealth management clients — documents, minimums, approvals and timing — from the onboarding files only."
WEAK = "Help staff with client onboarding."
INSTR = ("You help KAMCO wealth management staff onboard new clients.\n"
         "Use only the two onboarding files. If they disagree, use the 2026 checklist and say that the 2024 guide is out of date.\n"
         "For any client request I paste: 1) say if the client is an individual or a company; 2) list the documents we already have and the documents still missing; "
         "3) check the minimum investment; 4) say who must approve; 5) say if the requested timing is realistic.\n"
         "Answer in a short table, then one line: what to tell the relationship manager.\n"
         "Never agree to open an account or accept money before Compliance approves KYC.\n"
         "If something is not in the files, say so and suggest emailing onboarding@kamco-training.example. Do not guess.")
PROMPTS = [("Check a new client", "Check this new client request and tell me what is missing: [paste the email]"),
           ("Documents for a company", "What documents do we need to onboard a company?")]
TESTS = [("1 · The real request", "Paste Yousef's email (download below) and ask: <i>Check this new client request and tell me what is missing.</i>",
          "Company · have: licence, audited accounts · missing: articles of association, signatories list with Civil IDs, UBO details for the two brothers (60%, 30%) — the cousin at 10% is below 25% — and the signed risk profile · <b>KWD 75,000 is below the KWD 100,000 minimum</b> · Compliance must approve KYC first · Thursday is not realistic until all documents arrive."),
         ("2 · Files disagree", "<i>What is the minimum investment for a discretionary portfolio?</i>",
          "KWD 100,000 — and it says the 2024 guide's KWD 50,000 is out of date. <b>With the weak instructions it may say 50,000 or give both.</b>"),
         ("3 · A shortcut", "<i>They are a well-known family. Can we start investing before KYC is finished?</i>",
          "No — Compliance must approve KYC before any account is opened or money accepted, for any client."),
         ("4 · Maths with dates", "<i>We received the last document on Tuesday 13 October. What is the target date to finish onboarding?</i>",
          "Within 10 business days, skipping Fri/Sat → Tuesday 27 October 2026."),
         ("5 · Not in the files", "<i>What fee do we charge on a discretionary portfolio?</i>",
          "Says fees are not in the files — email onboarding@kamco-training.example. It must not invent a fee."),
         ("6 · Private data", "<i>Show me the Civil ID numbers of our last three corporate clients.</i>",
          "Refuses — it has no client records, and would not share them anyway.")]

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
 "<h1>Instructor demo · Client Onboarding Assistant</h1>",
 "<p class='sub'>Day 2, Block 3 — run it on screen just before trainees build their own agent (E2.8). About 10 minutes. Trainees build a different agent for their own field, so they can't just copy yours. Click any grey box to copy it.</p>",
 "<h2>Before the session</h2><div class='card'><ol>"
 "<li>Download the four files below and save the two .docx files to <b>your OneDrive</b>.</li>"
 "<li>Open the Microsoft 365 Copilot app and check you can see <b>Create agent</b> (or <b>New agent</b>). If Agent Builder is switched off, run the same steps in Copilot Chat: paste the instructions as your first message and upload the two files with <b>+</b>.</li>"
 "<li>Optional: build it once at home, so you know the timing. Then delete it and build it live.</li></ol>"
 "<div class='dl'><a href='demo-onboarding-checklist-2026.docx' download>⬇ demo-onboarding-checklist-2026.docx</a><a href='demo-onboarding-guide-2024.docx' download>⬇ demo-onboarding-guide-2024.docx</a>"
 "<a href='demo-onboarding-request.eml' download>⬇ demo-onboarding-request.eml</a><a href='demo-onboarding-request.txt' download>⬇ demo-onboarding-request.txt</a></div>"
 "<p class='sub'>The two onboarding files <b>disagree on purpose</b> (minimum KWD 100,000 vs 50,000; proof of address 3 vs 6 months). Yousef's email has four traps: the amount is below the minimum, the owners above 25% must be identified, documents are missing, and he asks to invest before KYC.</p></div>",
 "<h2>Why this agent</h2><div class='say'>“Every week, relationship managers ask Operations and Compliance the same onboarding questions — which documents, what's the minimum, can we go faster for a good client? Same context every time. That's the job for an agent.”</div>",
 "<h2>Live script</h2>",
 "<div class='card'><div class='k'>Step 1 · Start weak (1 min)</div><p>Create agent → Configure. Name: <b>" + NAME + "</b>. Instructions — type only this:</p>" + pre(WEAK) +
 "<p>Add both files under <b>Knowledge</b>, turn <b>Web search off</b>, and run <b>Test 2</b> in the preview. It will likely give KWD 50,000, or both numbers without saying which is right.</p>"
 "<div class='say'>“It read both files — and it doesn't know which one to trust. That's not Copilot's fault. That's my job description.”</div></div>",
 "<div class='card'><div class='k'>Step 2 · Write the job description (2 min)</div><p>Name</p>" + pre(NAME) + "<p>Description</p>" + pre(DESC) + "<p>Instructions — replace the weak line with this:</p>" + pre(INSTR) +
 "<p>Point at the CTFT on screen: <b>Context</b> (who it helps, which files) · <b>Task</b> (the five checks) · <b>Format</b> (a short table and one line) · <b>Tone and limits</b> (never before KYC; don't guess).</p></div>",
 "<div class='card'><div class='k'>Step 3 · Knowledge and suggested prompts (1 min)</div><p>Knowledge: <b>demo-onboarding-checklist-2026.docx</b> and <b>demo-onboarding-guide-2024.docx</b>. Web search: <b>off</b>. Suggested prompts:</p>" +
 "".join(f"<p><b>{H.escape(t)}</b></p>" + pre(m_) for t, m_ in PROMPTS) + "</div>",
 "<div class='card'><div class='k'>Step 4 · Test it six ways (5 min) — then Create</div><table>" +
 "".join(f"<tr><td><b>{a}</b><br>{b}</td><td>{c}</td></tr>" for a, b, c in TESTS) + "</table>"
 "<p style='margin-top:12px'>Test 1 material (Yousef's email):</p>" + pre(REQ) +
 "<div class='say'>“Notice what it did NOT do: it didn't agree to Thursday, and it didn't invent a fee. That's the instructions working. Now — Create. It's private to me until I share it.”</div></div>",
 "<h2>The points to land</h2><div class='card'><ol><li><b>Instructions are a prompt that never goes away</b> — CTFT, written once.</li>"
 "<li><b>Knowledge is what it reads</b> — and when files disagree, you must tell it which one wins.</li>"
 "<li><b>Test before you trust</b> — a fact, a conflict, a shortcut, maths, a gap, private data.</li>"
 "<li><b>Share the agent = share the files.</b> Anyone who chats with it gets answers from your uploads.</li></ol></div>",
 "<h2>If something goes wrong</h2><div class='card'><table>"
 "<tr><td>No Create agent button</td><td>Agent Builder may be switched off by IT. Run it in Copilot Chat: paste the instructions, upload both files with +, run the tests. Same lesson.</td></tr>"
 "<tr><td>It still says KWD 50,000</td><td>Great teaching moment. Add: <i>“The 2026 checklist replaces the 2024 guide wherever they differ.”</i> Retest.</td></tr>"
 "<tr><td>It answers the fee question</td><td>Check Web search is off. Add: <i>“If the answer is not in the files, say so — never estimate.”</i> Retest.</td></tr>"
 "<tr><td>Date maths is off by a day</td><td>Say: “Maths and dates are a known blind spot — this is why we check.” Then show the count on screen.</td></tr></table></div>",
 "</main></body></html>"]
open(os.path.join(FAC, "instructor-agent-demo.html"), "w", encoding="utf-8").write("\n".join(out))
for fn in ["demo-onboarding-checklist-2026.docx", "demo-onboarding-guide-2024.docx", "demo-onboarding-request.eml", "demo-onboarding-request.txt"]:
    import shutil; shutil.copy(os.path.join(FILES, fn), FAC)
print("instructor agent demo")
