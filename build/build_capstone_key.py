"""Facilitator page: capstone reference answers for the four fields (private — not on the public site)."""
import json, html as H
from capstone_lab import FIELDS, SPEC

cap = json.load(open("out/capstone.json"))
css = """:root{--bg:#00112F;--card:#0b2147;--line:#1d3a6b;--ink:#eef3ff;--dim:#a9b8d6;--blue:#4a87e8;--amber:#eab94a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 Inter,system-ui,sans-serif}
main{max-width:1000px;margin:0 auto;padding:32px 20px 60px}h1{font-size:30px;margin:0 0 6px}h2{font-size:22px;margin:34px 0 10px;color:var(--blue)}
.sub{color:var(--dim)}.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px;margin:14px 0}
table{width:100%;border-collapse:collapse}td{border-top:1px solid var(--line);padding:8px 6px;vertical-align:top}td:first-child{color:var(--dim);width:32%}
.k{font:600 12px/1 ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--amber);margin-bottom:8px}
nav a{color:var(--blue);margin-right:14px}pre{white-space:pre-wrap;background:#06183a;border:1px solid var(--line);border-radius:10px;padding:12px;font-size:13px;color:var(--dim)}
.rub td:first-child{width:12%;color:var(--amber);font-weight:700}"""
out = [f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Capstone answer key — KAMCO Copilot</title><style>{css}</style></head><body><main>",
       "<h1>Capstone · reference answers</h1><p class='sub'>Facilitator only — do not share. Lab task E2.9, 13:10 – 14:50. Pair presentations 14:50 – 15:00. Trainees pick a field; each reply should carry an executive brief (Word) and a 6-slide deck (PowerPoint) by 2:50 pm, subject “Capstone · [field] · [name]”.</p>",
       "<nav>" + "".join(f"<a href='#{k}'>{v}</a>" for k, v in FIELDS.items()) + "</nav>",
       "<div class='card rub'><div class='k'>Rubric · /100 · from the Program 2 outline · Pass / Does not pass</div><table>" + "".join(f"<tr><td>{w}</td><td><b>{n}</b> — {d}</td></tr>" for w, n, d in [
           (30, "Workflow completeness", "read the email, analysed the data, produced the brief and the deck, sent the reply by 2:50 pm. Pass: all steps attempted and submitted"),
           (25, "Data analysis accuracy", "Copilot output reviewed and corrected; numbers match the reference within rounding (traps below). Pass: no major data errors"),
           (20, "Deliverable quality", "brief (one page, bottom line first), deck (six slides, message titles) and charts are clear, professional and answer the request. Pass: presentation-ready"),
           (15, "AI review & judgement", "accuracy, confidentiality (the declined ask), tone, completeness; a real “What I corrected” line. Pass: at least one correction or verification noted"),
           (10, "Prompt quality", "the three prompts pasted at the end of the reply are specific, with context, task, format and tone. Pass: not generic")])+ "</table></div>"]
for k, name in FIELDS.items():
    key = cap["key"][k]; sp = SPEC[k]
    out.append(f"<h2 id='{k}'>{name}</h2>")
    out.append("<div class='card'><div class='k'>The request</div><table>" + "".join(f"<tr><td>{a}</td><td>{H.escape(b)}</td></tr>" for a, b in [
        ("Deadline", key["deadline"]), ("Deliverables", key["deliverables"]), ("Decline", key["decline"]),
        ("Brief for", H.unescape(sp["brief_to"])), ("Deck for", H.unescape(sp["deck_for"]))]) + "</table></div>")
    out.append("<div class='card'><div class='k'>Reference numbers</div><table>" + "".join(f"<tr><td>{H.escape(a)}</td><td>{H.escape(b)}</td></tr>" for a, b in key["numbers"]) + "</table></div>")
    out.append(f"<div class='card'><div class='k'>A good recommendation</div><p>{H.escape(key['recommend'])}</p></div>")
    out.append(f"<details class='card'><summary>Email thread · {H.escape(cap['threads'][k]['subject'])}</summary><pre>{H.escape(cap['threads'][k]['text'])}</pre></details>")
out.append("</main></body></html>")
open("out/facilitator/capstone-answer-key.html", "w", encoding="utf-8").write("\n".join(out))
print("capstone answer key")
