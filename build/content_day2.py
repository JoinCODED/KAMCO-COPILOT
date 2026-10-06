import json
from deckkit import *
from svgs import scene
from deckkit2 import map_slide

A = json.load(open("out/answers.json"))
M = A["murjan"]; W = A["waha"]


def kwd(x):
    return "KWD {:,.0f}".format(x)


S = []
CHECKS = []


def add(x):
    if len(x) == 3:
        CHECKS.append(dict(x[2], slide=len(S) + 1))
        S.append((x[0], x[1]))
    else:
        S.append(x)


BL = (f"Al-Murjan's portfolio was worth {kwd(M['total_sep'])} at 30 Sep, up {kwd(M['q3_change'])} ({M['q3_return_pct']:.1f}%) in Q3. "
      f"Equity is {M['alloc_pct']['Equity']:.1f}%, above the 55% maximum, and Al-Noor Bank is {M['issuer_top'][0][1]:.1f}% of the portfolio, above the 10% issuer limit. "
      "We recommend trimming equity, starting with Al-Noor Bank, and adding fixed income in line with the house view.")

# ================= OPENING =================
add(cover("Day 2", "AI at Work with", "Microsoft Copilot",
          "Day 2 · From Analysis to Reply. Yesterday's checked numbers become a memo, a deck and a reply you are proud to send.",
          "Day 2 · Mon 12 Oct 2026", "CODED Campus, Kuwait"))
poll = ('<div class="mini poll" style="max-width:880px"><div class="mini-q">It is 2:50 pm. Faisal is waiting. What would you rather receive?</div><div class="tag-opts" style="grid-template-columns:1fr 1fr">'
        '<button class="topt" data-fb="Most people pick B. The numbers are the same — the <b>work</b> is in turning them into an answer."><div class="tn">A · The 22-row spreadsheet</div><div class="tc">all the data, no message</div></button>'
        '<button class="topt" data-fb="Right — the reader wants the answer first. Today we build B, with Copilot, in minutes."><div class="tn">B · Three lines that answer the question</div><div class="tc">the answer first, the data behind it</div></button>'
        '</div><div class="mini-note"></div></div>')
add(hook("hook", "Day 2 · before we start", "Same numbers. <span class=\"hl\">Which one helps?</span>", poll,
         "Your Al-Murjan file from yesterday is today's raw material. Open it now."))
add(outcomes(2, ["Choose the right output — a <b>Word memo</b> or a <b>PowerPoint deck</b> — for the reader.",
                 "Use Copilot in Word to draft a one-page memo from <b>your checked numbers</b> and the house view.",
                 "Use Copilot in PowerPoint to turn the memo into a short deck where every title is <b>the message</b>.",
                 "Draft the Outlook reply and run the <b>four checks</b>: accuracy, confidentiality, tone, completeness.",
                 "Explain how an <b>agent</b> in Copilot Agent Builder can take over a repeated step."]))
add(road("The shape of Day 2", "Four topics, then <span class=\"hl\">your project.</span>",
         "Same rhythm as yesterday. After each topic, a lab challenge. After lunch, a short agent demo — then you complete one full request alone.",
         [("Memo or deck? Then Word", "Pick the format for the reader. Put the answer first."),
          ("PowerPoint", "One slide, one message — built from your memo."),
          ("Reply and review", "Draft the reply, then the four checks before you send."),
          ("From manual to agent", "Copilot Agent Builder: turn a repeated step into an agent."),
          ("Project · graded", "A new request, alone: email → analysis → memo or deck → reply."),
          ("MAP test and certificates", "See how far you came.")]))

# ================= TOPIC 1 =================
add(story(1, "Memo or deck? Then Word", "Fourteen slides",
          "The MD asked for “something for the Investment Committee”. You built fourteen beautiful slides. The committee reads every paper <b>at home, the night before</b>. They wanted <b>one page</b>. You start again at 9 pm.",
          "The wrong format is <span class=\"hl\">the most expensive mistake.</span>"))
add(analogy(1, 1, "Idea 1 of 2", "A letter or a speech.",
            "A <b>letter</b> is read alone, at the reader's pace, and must make sense without you. A <b>speech</b> is heard once, with you in the room to explain. Different jobs, different shapes.",
            scene("letter")))
add(term(1, 1, "This is <span class=\"hl\">memo or deck.</span>", "MEMO OR DECK",
         "A <b>memo</b> (Word) when the reader reads alone, needs detail, or decides later. A <b>deck</b> (PowerPoint) when you present live to a group and pictures help.",
         "Like the letter and the speech, ask <b>how it will be read</b>…", "Who reads it? How? What decision?",
         "The request usually tells you. <b>Read it again before you build.</b>"))
add(check(1, 1, "The Investment Committee reads every paper at home the night before the meeting. Which format?",
          [("A one-page Word memo", True, "Right. They read alone, at their own pace, and decide later — a memo carries the detail without you."),
           ("A 12-slide deck", False, "A deck needs a presenter. At home, it becomes a puzzle."),
           ("The Excel file — they can see everything", False, "The data is not the answer. They want your conclusion and the evidence.")]))
add(analogy(1, 2, "Idea 2 of 2", "The newspaper headline.",
            "A newspaper puts the most important fact in the <b>headline</b> and the first line. If you stop reading after one sentence, you still know what happened.",
            scene("headline")))
add(term(1, 2, "This is <span class=\"hl\">bottom line up front.</span>", "BOTTOM LINE UP FRONT",
         "Start with the answer and the action in two sentences. Then give the evidence: performance, allocation, issuer check, movers.",
         "Like the headline, the reader gets <b>the point first</b>…", "the rest is evidence they can check."))
add(demo(1, 3, "Live in Word · draft from your checked numbers", "Give Copilot <span class=\"hl\">your</span> numbers. Not its own.",
         "Copy the summary table from your Excel file into the prompt. Copilot writes; your numbers stay your numbers.",
         prompts([("Copilot in Word · Draft with Copilot", "Draft a one-page memo to Faisal Al-Mutairi about Al-Murjan Family Office's Q3. Use ONLY these figures: [paste your summary table from Excel]. Use /house-view-q4-2026.docx for the recommendation. Start with a two-sentence bottom line. Then short sections: Performance, Allocation vs mandate, Issuer check, Top and bottom contributors, Recommended actions. KWD without decimals, percentages to one decimal. Under 350 words. Internal memo, so no disclaimer.", "Every figure matches your Excel table."),
                  ("Copilot in Word · select a section → Rewrite", "Make this section shorter and more direct. Keep every number exactly as it is.", "Rewrite changes words, not numbers — check anyway."),
                  ("Copilot in Word · chat", "Check this memo against the request in Faisal's email: is anything missing?", "Use it as a second reader, then decide yourself.")])
         + f'<div class="keyline" style="margin-top:14px"><b>A strong bottom line</b> · {BL}</div>',
         bullets=["Paste the Excel summary table into the prompt — Copilot does not re-calculate.", "Reference the house view with /.", "Read the bottom line out loud."]))
add(check(1, 4, f"Copilot's memo says “equity is within the mandate”. Your Excel table says {M['alloc_pct']['Equity']:.1f}%, maximum 55%. What do you do?",
          [("Trust the memo — Copilot read the files", False, "Your checked table is the source of truth. The memo is a draft."),
           (f"Tell Copilot: “Equity is {M['alloc_pct']['Equity']:.1f}%, above the 55% maximum. Rewrite the allocation section.”", True, "Right. Correct it at the source and let Copilot rewrite around the fact."),
           ("Delete the allocation section", False, "The breach is the most important finding. It must be in the memo.")]))
add(pause(1))
add(case(1, "Six pages, <span class=\"hl\">read in silence.</span>", 6, "", 0, "Amazon · 2004",
         "Amazon's leaders replaced slide decks in senior meetings with <b>narrative memos of up to six pages</b>. Meetings start with everyone <b>reading in silence</b>. The reason given: writing full sentences forces clearer thinking than bullet points.",
         [(6, "", 0, "Pages, maximum"), (2004, "", 0, "Year of the change"), ("Silent", "", 0, "Reading starts the meeting")],
         "Next: when you do need slides — PowerPoint →"))
add(take(1, "Topic 1 · the habit", "Pick the format for the reader. <b>Answer first.</b> Feed Copilot numbers you have checked.",
         say="Lab challenges 1 and 2 now: Memo or deck, then Answer first. 10 minutes."))

# ================= TOPIC 2 =================
add(story(2, "PowerPoint", "The deck nobody remembered",
          "Twelve slides. Nine bullets each. Every number was right. After the meeting, the client could not say <b>what the main point was</b>. Neither could the RM.",
          "A slide that says everything <span class=\"hl\">says nothing.</span>"))
add(analogy(2, 1, "Idea 1 of 2", "Road signs.",
            "A road sign gives <b>one message</b> you can read at speed: “Exit 3 →”. Imagine a sign with nine lines of text. You would miss your exit.",
            scene("sign")))
add(term(2, 1, "This is <span class=\"hl\">one slide, one message.</span>", "ONE SLIDE, ONE MESSAGE",
         "Each slide title is a full sentence that states the message. The body is only the evidence for that sentence — a chart or two or three points.",
         "Like the road sign, readable <b>at speed</b>…", "if they read only the titles, they still get the story."))
flips = [("Q3 Performance", f"The portfolio grew {M['q3_return_pct']:.1f}% in Q3, to {kwd(M['total_sep'])}"),
         ("Asset Allocation", f"Equity is {M['alloc_pct']['Equity']:.1f}% — above the 55% mandate maximum"),
         ("Issuer Exposure", f"Al-Noor Bank is {M['issuer_top'][0][1]:.1f}% of the portfolio — above the 10% limit"),
         ("Next Steps", "We recommend trimming equity, starting with Al-Noor Bank")]
fl = '<div class="flip-row">' + "".join(
    f'<div class="flip-card"><div class="flip-inner"><div class="flip-face flip-front"><div class="tapme">weak title · tap</div><div class="ft">{a}</div><div class="tapme">→ flip</div></div><div class="flip-face flip-back"><div class="bt">Message title</div><div class="bd">{b}</div></div></div></div>'
    for a, b in flips) + '</div><div class="flip-allnote">Read only the four back sides: that is the whole client meeting.</div>'
add(demo(2, 1, "Live demo · fix the titles", "Four weak titles. <span class=\"hl\">Flip each one.</span>",
         "A topic is not a message. Tap each card to see the title rewritten as the message.", fl,
         bullets=["Flip each card. Read the back sides in order.", "Point: the four titles alone tell the client story."]))
add(analogy(2, 2, "Idea 2 of 2", "The architect's sketch.",
            "An architect does not start with bricks. They sketch the outline first, agree it, and <b>then</b> build. Your memo is the sketch; the deck is the building.",
            scene("sketch")))
add(term(2, 2, "This is <span class=\"hl\">a deck from a file.</span>", "CREATE FROM FILE",
         "In PowerPoint, ask Copilot to create a presentation from a Word document. Then refine: change titles, add or remove slides, add speaker notes, and apply your company template.",
         "Like the sketch, the memo is <b>already agreed</b>…", "so the deck follows the same story — and the same numbers."))
add(demo(2, 3, "Live in PowerPoint · from memo to deck", "Four prompts. <span class=\"hl\">Five slides.</span>",
         "Save yesterday's memo in OneDrive first. Then open a new presentation and run these.",
         prompts([("Copilot in PowerPoint", "Create a presentation from /AMFO-Q3-memo.docx with 5 slides: 1) the headline summary, 2) Q3 performance, 3) allocation against the mandate, 4) the issuer check, 5) recommendation and next steps.", "Five slides, same numbers as the memo."),
                  ("Copilot in PowerPoint", "Change every slide title to one full sentence that states the main message of the slide.", "Read the titles only — do they tell the story?"),
                  ("Copilot in PowerPoint", "Add speaker notes to each slide, under 60 words each, in plain English for a family CFO.", "Notes help the RM who presents."),
                  ("Excel → PowerPoint", "Copy your allocation chart from Excel and paste it on slide 3. Add the source under it: Custody export, 30 Sep 2026.", "Charts you made beat charts it guessed.")]),
         bullets=["Run live with the Al-Murjan memo.", "Show the titles view (Outline) after prompt 2.", "Paste a real Excel chart on slide 3."]))
add(check(2, 4, "Slide 3 has the title “Allocation”, a chart without a source, and eight bullets. What do you fix first?",
          [("Add more colour so it stands out", False, "Design does not fix a missing message."),
           ("Make the title the message, add the source, cut to three points", True, "Right. Message first, evidence second — and every chart shows its source."),
           ("Split it into two slides of four bullets", False, "Now you have two slides with no message.")]))
add(pause(2))
add(case(2, "The warning was <span class=\"hl\">on a slide.</span>", 2003, "", 0, "Space Shuttle Columbia · 2003",
         "The investigation board found that engineers' concerns about foam damage were presented in <b>dense PowerPoint slides</b>, where the key warning was buried low in the bullets. The board criticised the <b>“endemic use of PowerPoint briefing slides instead of technical papers.”</b>",
         [(7, "", 0, "Crew members lost"), (2003, "", 0, "Year"), ("1 line", "", 0, "Where the warning sat")],
         "Next: the reply — and the four checks →"))
add(take(2, "Topic 2 · the habit", "Write each title as <b>the message</b>. Build the deck from <b>your memo</b>, not from scratch.",
         say="Lab challenge 3 now: Fix the deck. 5 minutes."))

# ================= TOPIC 3 =================
add(story(3, "Reply and review", "2:49 pm",
          "The reply goes out one minute before the deadline. The deck is attached. The email says returns <b>“will stay strong”</b>, quotes last week's number, and mentions <b>another family by name</b>. It took Copilot ten seconds to write. It will take weeks to repair.",
          "Copilot writes the reply. <span class=\"hl\">You sign it.</span>"))
add(analogy(3, 1, "Idea 1 of 2", "The pilot's pre-flight checklist.",
            "Pilots with twenty years of experience still use the checklist <b>before every flight</b>. Not because they forget — because the checklist <b>catches what experience misses</b> on a busy day.",
            scene("checklist")))
add(term(3, 1, "These are <span class=\"hl\">the four checks.</span>", "THE FOUR CHECKS",
         "<b>Accuracy</b>: every number matches your analysis. <b>Confidentiality</b>: only this client, only the right people. <b>Tone</b>: fits the reader, no promises. <b>Completeness</b>: everything asked for, attachment, people copied, disclaimer if needed.",
         "Like the checklist, <b>every send, every time</b>…", "you sign the email, not Copilot."))
rep = (f'<p>Dear Reem,</p><p>Please find the Al-Waha Q3 memo attached. Total value at 30 Sep was {hot(kwd(W["total_sep"]), False, "Correct — matches the analysis.")}. '
       + hot("Real estate is 5.4% of the portfolio, inside the mandate.", True, "ACCURACY — it is 4.5%, below the 5% minimum. Digits swapped, conclusion wrong.")
       + f' {hot("Gulf Trade Bank is 11.8% of the portfolio, above the 10% limit.", False, "Correct — this one is fine.")}</p><p>'
       + hot("We used the same approach as for the Al-Murjan family last month.", True, "CONFIDENTIALITY — never name another client.")
       + ' ' + hot("We are confident returns will stay strong next quarter.", True, "TONE — never promise or imply future returns.")
       + '</p><p>' + hot("I will send the issuer table separately next week.", True, "COMPLETENESS — the issuer check was part of the request, due today.")
       + '</p><p>Best regards</p>')
add(demo(3, 1, "Live demo · run the four checks", "An AI-drafted reply. <span class=\"hl\">Four problems.</span>",
         "Copilot drafted this reply to Reem in seconds. Click every sentence that fails one of the four checks.",
         mailbox("Outlook · Draft", "You", "Reem Al-Qattan", "RE: Al-Waha FO - Q3 numbers for the family meeting", rep, attach="AWFO-Q3-memo.docx")
         + '<div class="foundct">Problems found <b>0</b> / 4</div><div class="mini-note hotnote" data-def="Two sentences are correct. Do not flag them."></div>'
         + '<div class="keyline hotwin" style="display:none">Accuracy · confidentiality · tone · completeness. <b>One of each — in a six-line email.</b></div>',
         bullets=["4 problems: 5.4% (is 4.5%), names Al-Murjan, promises returns, issuer table 'next week'.", "2 correct sentences: the total value and Gulf Trade Bank 11.8%."]))
add(analogy(3, 2, "Idea 2 of 2", "Answering in the guest's language.",
            "When a guest greets you formally, you answer formally. When a colleague writes three warm lines, you do not answer with a legal letter. <b>Match the voice you were given.</b>",
            scene("greet")))
add(term(3, 2, "This is <span class=\"hl\">Draft and Coaching.</span>", "DRAFT · COACHING BY COPILOT",
         "In Outlook, <b>Draft with Copilot</b> writes a reply from your instructions. <b>Coaching by Copilot</b> reviews your draft for tone, clarity and the reader's feelings — and suggests changes.",
         "Like answering in the guest's language, <b>match the sender</b>…", "then read it as the client would."))
add(demo(3, 3, "Live in Outlook · draft, coach, check", "The reply to <span class=\"hl\">Faisal.</span>",
         "Reply on the Al-Murjan thread. Attach your deck and memo before you ask Copilot.",
         prompts([("Copilot in Outlook · Draft with Copilot", "Draft a reply to Faisal. Say the 5-slide client deck and the one-page memo are attached. Give the three key findings in one line each: Q3 value and change, the equity breach, and the Al-Noor Bank issuer breach. Say Noura in Compliance is copied. Under 100 words, professional and warm.", "Every number matches your Excel table."),
                  ("Copilot in Outlook · Coaching by Copilot", "(Click Coaching by Copilot on your draft.)", "Accept only the suggestions that fit Faisal's tone."),
                  ("You · the four checks", "Accuracy · Confidentiality · Tone · Completeness", "Attachments on? Noura copied? No other client named? No promise of returns?")]),
         bullets=["Attach the files first.", "Run Draft, then Coaching.", "Read the four checks out loud before Send."]))
add(check(3, 4, "Copilot added: “We expect strong returns to continue next quarter.” Keep it?",
          [("Yes — it sounds positive and the client will like it", False, "It implies a promise about future returns. The house view rules forbid it."),
           ("No — remove it. Never promise or imply future returns", True, "Right. Positive tone is fine; promises are not. Delete the sentence."),
           ("Keep it, but add “we think”", False, "Still an implied forecast in a client-facing message. Remove it.")]))
add(pause(3))
add(case(3, "A government report, <span class=\"hl\">a partial refund.</span>", "A$440k", "", 0, "Deloitte Australia · 2025",
         "A report Deloitte prepared for an Australian government department was found to contain <b>AI-generated errors</b>, including references that did not exist and an invented quote from a court judgment. Deloitte agreed to <b>refund part of its fee</b>.",
         [("A$440k", "", 0, "Contract value"), (2025, "", 0, "Year"), ("Refund", "", 0, "Part of the fee")],
         "Next: from manual work to an agent →"))
add(take(3, "Topic 3 · the habit", "Run the four checks <b>before every send</b>. Accuracy · Confidentiality · Tone · Completeness.",
         say="Lab challenges 4 and 5 now: Check the reply, then Name the check. 15 minutes. Then lunch."))

# ================= TOPIC 4 =================
add(story(4, "From manual to agent", "Every Sunday",
          "Every Sunday, Faisal's team receives forty client requests. Someone reads each one to find the client, the ask, the deadline and the risks. <b>Same steps, every week</b> — and every week someone misses a changed deadline.",
          "A repeated job is a job for <span class=\"hl\">an agent.</span>"))
add(analogy(4, 1, "Idea 1 of 1", "The job description.",
            "When you hire someone, you write a job description: the <b>role</b>, the <b>rules</b>, the <b>files</b> they use, and what a good result looks like. Then you test them before you trust them.",
            scene("jobdesc")))
add(term(4, 1, "This is <span class=\"hl\">an agent.</span>", "AGENT (COPILOT AGENT BUILDER)",
         "A version of Copilot set up for one repeated job, with its own <b>instructions</b> (the job description), <b>knowledge</b> (the files it uses) and <b>starter prompts</b>. You build it in the Microsoft 365 Copilot app with <b>Create agent</b>.",
         "Like a job description, <b>clear role, clear rules</b>…", "an agent is only as good as its <b>instructions</b>.",
         "Automate the repeat. <b>Keep the judgement.</b>"))
add(flow("t4d1", "Live demo · Copilot Agent Builder", "Build a <span class=\"hl\">Request Triage Assistant.</span>",
         "The instructor builds it live. If Agent Builder is switched off for your account, watch the demo — the steps are the same.",
         [("01", "Create agent", "Copilot app → Agents → Create agent"), ("02", "Describe", "Name: Request Triage Assistant. One-line purpose."),
          ("03", "Instructions", "The job description — see the next slide"), ("04", "Knowledge", "Add the house view and the mandate rules"),
          ("05", "Test, fix, share", "Paste the Al-Waha thread. Fix the instructions. Share.")],
         "Five steps", t="t4"))
add(demo(4, 2, "Live demo · the instructions", "The job description <span class=\"hl\">is the agent.</span>",
         "Paste these into the Instructions box. Then test the agent with the Al-Waha thread and the Al-Murjan thread.",
         prompts([("Agent Builder · Instructions", "You help KAMCO wealth management staff read client requests. For any email or thread I paste: 1) give the client name; 2) list each requested output and its format; 3) give the final deadline - always use the newest message when instructions change; 4) list who must be copied; 5) flag any request that breaks our client communication rules, such as sharing another client's data or promising returns. Answer in a table. If something is unclear, say so - do not guess.", "Short, specific, testable rules."),
                  ("Agent Builder · Knowledge", "house-view-q4-2026.docx (section 4: rules for client communication)", "The agent checks requests against your rules."),
                  ("Agent Builder · Test", "[Paste the Al-Murjan thread] Triage this request.", "Does it catch the Tuesday deadline and the other-family request?")]),
         bullets=["Paste the instructions; add the house view as knowledge.", "Test with both threads.", "Show one fix: tighten a rule and re-test."]))
add(check(4, 3, "Your agent says the Al-Murjan deadline is Wednesday. The newest message says Tuesday, 3:00 pm. What do you fix?",
          [("Nothing — agents make mistakes sometimes", False, "If you know the cause, fix it — otherwise it repeats every week."),
           ("The instructions: “Always use the newest message when instructions change.”", True, "Right. The instructions are the job description. Make the rule explicit and test again."),
           ("Delete the agent and do it by hand", False, "One fix and a re-test is faster than giving up.")]))
add(case(4, "Two-thirds of the chats — <span class=\"hl\">and then the humans came back.</span>", "2/3", "", 0, "Klarna · 2024–2025",
         "Klarna said its AI assistant handled <b>two-thirds of customer service chats</b> in its first month — about the work of 700 full-time agents. In 2025 the company said it would make sure customers can <b>always reach a human</b>, because quality matters.",
         [(2.3, "M", 1, "Chats in month one"), (700, "", 0, "Full-time agents' work, claimed"), (2025, "", 0, "Human option restored")],
         "Next: your project →"))
add(take(4, "Topic 4 · the habit", "Automate the <b>repeat</b>. Keep the <b>judgement</b>. Test before you trust.",
         say="Brief the project now (next slide), then start the clock at 13:30."))

# ================= PROJECT, MAP, CERTIFICATES =================
rub = '<div class="rub b in">' + "".join(f'<div><div class="w">{w}</div><div class="n">{n}</div></div>' for w, n in [(30, "Workflow complete"), (25, "Accurate numbers"), (20, "Deliverable quality"), (15, "AI review & judgement"), (10, "Prompt quality")]) + '</div>'
add(standby("project", "Project · graded · 80 minutes", "One request. <span class=\"hl\">Alone. Start to finish.</span>",
            "At 13:30 a new email arrives in your inbox — version A or version B. Treat it like a real request from a KAMCO manager.",
            ["<b>Read</b> the email with Copilot in Outlook. Write down the deadline and the deliverable.",
             "<b>Clean and analyse</b> the attached custody export in Excel. Check every formula.",
             "<b>Produce</b> the deliverable: <b>A = one-page Word memo</b> · <b>B = 5-slide PowerPoint deck</b>.",
             "<b>Reply</b> to the email with your file attached by <b>2:50 pm</b>. Add one line at the end: “What I corrected: …”",
             "<b>Finished early?</b> Build the other format too (A → a 3-slide deck, B → a one-page memo) — it is not graded, but it is great practice."],
            "13:30 – 14:50 · break when you need it", extra=rub, t="t4", k="demo",
            say="Graded on the five criteria shown. Replies arrive in the evaluation inbox with a timestamp. No help from neighbours — help from Copilot is the point."))
add(map_slide("mapend", "Before we close · 15:00", "MAP test — <span class=\"hl\">see your progress.</span>", 30, "post", t="close"))
add(standby("cert", "15:30 · certificates", "Well done. <span class=\"hl\">Certificates.</span>",
            "Two days, one real job — from a request in your inbox to a reply you can stand behind.",
            ["Certificates are handed out by name.", "Evaluation results for <b>AI in Investments (Program 3)</b> follow from KAMCO and CODED.", "Please complete the short feedback survey before you leave."],
            None, t="close"))
add(close("Two days, one job", "Request → Check → Produce → <span class=\"hl\">Reply.</span>",
          "You can now find the real ask, check the numbers, build the right output and send a reply that passes the four checks — with Copilot doing the heavy lifting and <b>you doing the judging</b>.",
          "Next: AI in Investments (Program 3)"))
