"""Scenario emails (single source for .eml files, the website case pages, labs and the facilitator kit)."""

MD = "Faisal Al-Mutairi"
MD_ROLE = "Managing Director, Wealth Management"

# ---------- Teaching scenario (trainees) ----------
MURJAN_THREAD = dict(
  subject="RE: FW: Al-Murjan FO - Q3 review pack",
  attach="amfo-q3-custody-export.xlsx",
  msgs=[
    dict(frm=MD + " (" + MD_ROLE + ")", when="Sun 11 Oct 2026, 08:12", to="You", body=
"""Hi,

Small change - see Khalid's note below. The client has moved the meeting to Wednesday 14 Oct at 11:00, so I need the pack from you by Tuesday 13 Oct, 3:00 pm, not Wednesday.

Use the custody export attached (30 Sep). Do not use the June factsheet - those numbers are out of date.

Please keep it to a 5-slide deck for the client and a one-page memo for me. Copy Noura in Compliance before anything goes to the client.

Thanks,
Faisal"""),
    dict(frm="Khalid Al-Murjan (CFO, Al-Murjan Family Office)", when="Sat 10 Oct 2026, 19:40", to=MD, body=
"""Dear Faisal,

Apologies - I need to move our review to Wednesday 14 Oct, 11:00, same place.

The family is asking two things in particular: how much of the portfolio now sits with Al-Noor Bank after its strong quarter, and whether we are still inside the mandate on equities.

Also, could you send last quarter's report for the Al-Rumaithiya family account, so we can see your reporting format?

Best regards,
Khalid"""),
    dict(frm=MD + " (" + MD_ROLE + ")", when="Thu 8 Oct 2026, 10:05", to="You", body=
"""Hi,

Please prepare the Q3 review pack for Al-Murjan Family Office for the client meeting on Thursday 15 Oct. I need:

1) Portfolio value at 30 Sep and the Q3 change (KWD and %)
2) Allocation against the mandate - flag anything outside the range
3) Single-issuer check against the 10% limit
4) Top 3 and bottom 3 contributors for the quarter

Send me the pack by Wednesday 14 Oct.

Faisal"""),
  ])

# ---------- Instructor demo scenario ----------
WAHA_THREAD = dict(
  subject="RE: Al-Waha FO - Q3 numbers for the family meeting",
  attach="awfo-q3-custody-export.xlsx",
  msgs=[
    dict(frm="Reem Al-Qattan (Head of Client Advisory)", when="Sun 11 Oct 2026, 07:55", to="You", body=
"""Hi,

Update: the family wants a short memo only - no slides this time. Please send it to me by Monday 12 Oct, 1:00 pm.

They are worried about property. Please check real estate against the mandate first, then the rest of the allocation, and the 10% issuer limit.

Use the 30 Sep custody export attached.

Thanks,
Reem"""),
    dict(frm="Reem Al-Qattan (Head of Client Advisory)", when="Wed 7 Oct 2026, 14:20", to="You", body=
"""Hi,

Al-Waha Family Office meets us next week. Please prepare a 4-slide deck with the Q3 value, the Q3 change, allocation against the mandate and the top contributors. I need it by Thursday 15 Oct.

Reem"""),
  ])

# ---------- Day 1 inbox triage (trainee lab) ----------
TRIAGE = [
  dict(frm="Noura Al-Rashidi", em="n.alrashidi@kamco-training.example", subj="Reminder: Q3 suitability attestations due today 5:00 pm",
       body="Hi all, a reminder that your Q3 suitability attestations are due in the compliance portal today by 5:00 pm. Late attestations are escalated to the CEO office. Noura", key="now"),
  dict(frm="Operations Desk", em="ops.desk@kamco-training.example", subj="Failed settlement - Gulf Trade Bank trade, confirm SSI by 2:00 pm",
       body="The GTB sale for Al-Murjan FO failed to settle this morning. Please confirm the standing settlement instructions with the client by 2:00 pm today so we can re-submit. Ops", key="now"),
  dict(frm=MD, em="f.almutairi@kamco-training.example", subj="RE: FW: Al-Murjan FO - Q3 review pack",
       body="Small change - the client moved the meeting to Wednesday 14 Oct, so I need the pack by Tuesday 13 Oct, 3:00 pm. Deck plus one-page memo. Faisal", key="plan"),
  dict(frm="Yousef Al-Kandari", em="y.alkandari@kamco-training.example", subj="Client asks for a call this week on the bond ladder",
       body="Dar Al-Sanad's trustees would like a 30-minute call before Thursday about extending the bond ladder. Can you suggest two time slots? Yousef", key="plan"),
  dict(frm="Investment Strategy & Research", em="research@kamco-training.example", subj="Published: Q4 2026 House View",
       body="The Q4 2026 House View is now on the research portal. No action needed - please read before your next client meeting. Research team", key="fyi"),
]
TRIAGE_OPTS = [dict(k="now", l="Do now (due today)"), dict(k="plan", l="Plan (due this week)"), dict(k="fyi", l="FYI (no action)")]

TRIAGE_I = [  # instructor version
  dict(frm="IT Service Desk", em="it.desk@kamco-training.example", subj="Your Copilot licence is active - sign in today to confirm",
       body="Please sign in to Copilot today and type Hello to confirm your licence works before the training. IT", key="now"),
  dict(frm="Reem Al-Qattan", em="r.alqattan@kamco-training.example", subj="RE: Al-Waha FO - Q3 numbers for the family meeting",
       body="Update: memo only, no slides. Please send it to me by Monday 12 Oct, 1:00 pm. Real estate first. Reem", key="plan"),
  dict(frm="Finance", em="finance@kamco-training.example", subj="Expense claims close today at 3:00 pm",
       body="September expense claims must be submitted today by 3:00 pm to be paid this month. Finance", key="now"),
  dict(frm="Marketing & IR", em="ir@kamco-training.example", subj="New photos for the investor relations page",
       body="We updated the leadership photos on the investor relations page. Nothing needed from you. IR team", key="fyi"),
  dict(frm="Hessa Al-Fadhli", em="h.alfadhli@kamco-training.example", subj="Can we review the new client onboarding form this week?",
       body="Could you give me 20 minutes before Wednesday to review the new onboarding form? Hessa", key="plan"),
]

# ---------- Project emails (Day 2, graded) ----------
PROJECT_A = dict(
  version="A", client="Al-Bayan Holding", attach="abh-q3-custody-export.xlsx", output="Word memo",
  subject="Al-Bayan Holding - Q3 memo for the Investment Committee (today)",
  frm="Huda Al-Enezi (Investment Committee Secretary)", when="Mon 12 Oct 2026, 13:30", body=
"""Hi,

The Investment Committee will review Al-Bayan Holding tomorrow morning. Please send me a one-page memo in Word, attached to your reply, by 2:50 pm today.

The memo must cover:
1) Portfolio value at 30 Sep and the Q3 change (KWD and %)
2) Allocation against the mandate, with any breach clearly flagged
3) The 10% single-issuer check
4) The top 3 contributors for the quarter
5) Your recommendation in one or two sentences

Use the 30 Sep custody export attached. This is internal, so no client disclaimer is needed - but please keep it to one page.

Thanks,
Huda""")

PROJECT_B = dict(
  version="B", client="Dar Al-Sanad Trust", attach="dast-q3-custody-export.xlsx", output="PowerPoint deck",
  subject="Dar Al-Sanad Trust - 5-slide Q3 deck for the trustees (today)",
  frm="Yousef Al-Kandari (Senior Relationship Manager)", when="Mon 12 Oct 2026, 13:30", body=
"""Hi,

I am meeting the Dar Al-Sanad trustees tomorrow. Please send me a 5-slide PowerPoint deck, attached to your reply, by 2:50 pm today.

The deck must cover:
1) Portfolio value at 30 Sep and the Q3 change (KWD and %)
2) Allocation against the mandate, with any breach clearly flagged
3) The 10% single-issuer check
4) The top 3 contributors for the quarter
5) A clear recommendation on one slide

Use the 30 Sep custody export attached. This goes to the client, so add our standard disclaimer from the house view document.

Thanks,
Yousef""")


def thread_text(t):
    parts = []
    for m in t["msgs"]:
        parts.append("From: %s\nSent: %s\nTo: %s\n\n%s" % (m["frm"], m["when"], m["to"], m["body"]))
    return ("\n\n" + "-" * 40 + "\n\n").join(parts)
