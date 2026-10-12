import os
from build_pages import panel_page, res
pub=[("index.html","Landing · the programme"),("coded-kamco-day-1.html","Day 1 page"),("coded-kamco-day-1-deck.html","Day 1 slide deck (71 slides)"),("coded-kamco-day-1-lab.html","Day 1 trainee lab (7 challenges)"),
     ("coded-kamco-day-2.html","Day 2 page"),("coded-kamco-day-2-deck.html","Day 2 slide deck (49 slides)"),("coded-kamco-day-2-lab.html","Day 2 trainee lab (6 challenges)"),
     ("case-files.html","Case files · Al-Murjan thread and downloads"),("before-you-start.html","Before you start · sign-in, backup, fallbacks"),("cheat-sheet.html","Cheat sheet"),
     ("amfo-q3-custody-export.xlsx","Al-Murjan custody export"),("01-amfo-q3-review-request.eml","Al-Murjan thread (.eml)"),("house-view-q4-2026.docx","House view Q4 2026")]
fac=[("instructor-agent-demo.html","Instructor agent demo · Client Onboarding Assistant: files, script, six tests"),("run-of-show.html","Run of show, lead/support, readiness checklist, Day 1 email"),("capstone-answer-key.html","Capstone · four fields: requests, reference answers, rubric"),("project-and-scoring.html","Earlier project A/B emails and reference answers (replaced by the capstone)"),("kamco-p2-scoring-sheet.xlsx","Scoring sheet · 35 trainees, auto-total and rank")]
for d in (1,2):
    fac+=[(f"coded-kamco-day-{d}-notes.html",f"Day {d} presenter notes"),(f"coded-kamco-day-{d}-answer-key.html",f"Day {d} demos & answer key"),(f"coded-kamco-day-{d}-walkthrough.html",f"Day {d} trainee lab walkthrough"),
          (f"coded-kamco-day-{d}-instructor-lab.html",f"Day {d} instructor demo lab (Al-Waha)"),(f"coded-kamco-day-{d}-instructor-solutions.html",f"Day {d} instructor demo solutions")]
fac+=[("awfo-q3-custody-export.xlsx","Al-Waha export (instructor demos)"),("00-awfo-instructor-demo-request.eml","Al-Waha thread"),("project-A-al-bayan-request.eml","Project A email"),("abh-q3-custody-export.xlsx","Project A export"),("project-B-dar-al-sanad-request.eml","Project B email"),("dast-q3-custody-export.xlsx","Project B export")]
def lst(items, zipname):
    return '<p>Clean URL = the file name without .html once deployed. Package: <b>'+zipname+'</b>.</p><div class="res-list">'+"".join(res(f,l,f.rsplit('.',1)[1].upper() if not f.endswith('.html') else '/'+f[:-5]).replace(' download>','>') for f,l in items)+'</div>'
html=panel_page("Workshop index — KAMCO Copilot","Facilitator · every deliverable","Workshop index","AI at Work with Microsoft Copilot · CODED × KAMCO Invest · Sun 11 – Mon 12 Oct 2026.",
  [("Public site (share with trainees)",lst(pub,"kamco-copilot-site.zip")),("Facilitator kit (Aya & Ali only)",lst(fac,"kamco-copilot-facilitator.zip")),
   ("Not built yet",'<p>MAP tests (pre and post) — add the links to the deck slides 2 (Day 1) and 47 (Day 2) once ready. Backup-account credentials go in the onboarding email, not on the site.</p>')])
open("out/facilitator/workshop-index.html","w").write(html)
