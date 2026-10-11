"""Day 1 deck — block structure (Mastering Copilot flow) with KAMCO investment content."""
import json
from deckkit import *
from deckkit2 import *
from svgs import scene
from emails import WAHA_THREAD
from scenarios import MANDATE

A = json.load(open("out/answers.json"))
W = A["waha"]
LAB = "coded-kamco-day-1-lab.html"


def kwd(x):
    return "KWD {:,.0f}".format(x)


S = []; CHECKS = []


def add(x):
    if len(x) == 3:
        CHECKS.append(dict(x[2], slide=len(S) + 1)); S.append((x[0], x[1]))
    else:
        S.append(x)


# ===================== OPENING =====================
add(cover("Day 1", "AI at Work with", "Microsoft Copilot",
          "Day 1 · From Inbox to Insight. One investment request, followed from the first email to a clean, checked analysis in Excel.",
          "Day 1 · Sun 11 Oct 2026 · 09:00 – 16:00", "CODED Campus, Kuwait",
          say="Welcome everyone. Two days, one real piece of work: a client request, from the email to the reply."))
add(map_slide("map", "Before we begin · 09:00", "The <span class=\"hl\">MAP test.</span>", 30, "pre",
              say="Start the timer. While they work, walk the room and check who cannot sign in to Copilot — hand out backup accounts."))
poll = ('<div class="mini poll" style="max-width:760px"><div class="mini-q">How long would this take you today?</div><div class="tag-opts" style="grid-template-columns:repeat(4,1fr)">'
        + "".join(f'<button class="topt" data-fb="{fb}"><div class="tn">{t}</div></button>' for t, fb in [
            ("&lt; 1 hour", "Fast. Today we check that fast is also <b>right</b>."),
            ("1–3 hours", "That is most of the room. Let us see which parts Copilot can take."),
            ("Half a day", "Where does the time go? Usually cleaning the data and rewriting."),
            ("A full day", "Then this program pays for itself on the first request.")])
        + '</div><div class="mini-note"></div></div>')
add(hook("hook", "Day 1 · 09:30", "A request lands at <span class=\"hl\">08:12 on a Sunday.</span>",
         mailbox("Outlook · Inbox", "Faisal Al-Mutairi (MD, Wealth Management)", "You", "Al-Murjan FO - Q3 review pack",
                 "<p>Please prepare the Q3 review pack for Al-Murjan Family Office: portfolio value and Q3 change, allocation against the mandate, the 10% issuer check, and the top and bottom contributors. Deck for the client, one-page memo for me.</p>",
                 attach="amfo-q3-custody-export.xlsx").replace('class="mail"', 'class="mail" style="max-width:720px;margin:0 auto 14px"') + poll,
         "Hold your answer. By tomorrow afternoon you will do this whole job with Copilot — and check every number.",
         say="Ask for a show of hands first, then click the most common answer."))
add(wall_slide("ice", "Ice breaker · 5 minutes", "What is one task that <span class=\"hl\">eats your week?</span>",
               "Name, department — and one task that takes far too much of your time. We pin every answer on the wall and come back to it at the end of the day.",
               "e.g. building the monthly client report", "tasks",
               say="Go round the room quickly. Type each task as people say it. Keep it to one line each."))
add(outcomes(1, ["Explain what AI and large language models are — and what they <b>cannot</b> do.",
                 "Use Copilot safely with client data, with your <b>work</b> account.",
                 "Write prompts with <b>Context, Task, Format and Tone</b> for investment work.",
                 "Find the real deadline and deliverable in a long Outlook thread.",
                 "Clean a custody export in <b>Excel</b>, check it against the mandate, and explain every number."]))
add(standby("setup", "Setup check · 3 minutes", "Can you reach <span class=\"hl\">Copilot?</span>", "Do this now — before we start the first block.",
            ["Open <b>copilot.cloud.microsoft</b> (or m365copilot.com).", "Sign in with your <b>KAMCO work account</b> — never a personal one.", "Type <b>Hello</b> and press Enter. An answer back? You are ready.", "Stuck? Raise your hand — we have backup accounts."],
            None, say="Ali walks the room. Anyone without Copilot gets a backup account now."))

# ===================== BLOCK 1 · AI → LLM → COPILOT =====================
add(wall_slide("b1ask", "Block 1 · What is AI?", "In one line: what is <span class=\"hl\">Artificial Intelligence?</span>",
               "No wrong answers. Call it out — we pin it, then compare with the definition.", "e.g. a computer that thinks", "ai", t="t1",
               say="Collect 5–6 answers. Do not correct anyone yet — the next slide does that."))
add(cards_slide("b1def", "t1", "term", "Start here", "So what <span class=\"hl\">is</span> AI?",
                "<b>Software that learns patterns from examples</b> — and uses them to predict, sort, recommend or create — instead of only following rules a person wrote.",
                [dict(i="📈", t="Predict", d="What is likely next — a price move, a late payment, the next word."),
                 dict(i="🗂️", t="Classify", d="Which bucket — fraud or normal, urgent or not, equity or bond."),
                 dict(i="🎯", t="Recommend", d="What fits — a product, a film, a portfolio for a risk profile."),
                 dict(i="✍️", t="Create", d="New text, images or code — this is <b>generative AI</b>.")],
                nots=["Not magic", "Not always right", "Not a decision-maker"], cols=4,
                say="Compare with the wall: who was closest? The key word is 'learns'."))
add(cards_slide("b1ex", "t1", "story", "Prime examples", "You already use AI <span class=\"hl\">every day.</span>", None,
                [dict(i="💳", t="Card fraud alerts", d="Your bank flags an unusual payment in seconds."),
                 dict(i="🏦", t="Credit scoring", d="A model predicts the chance a loan is repaid."),
                 dict(i="📊", t="Robo-advisers & trading", d="Models suggest portfolios or execute trades by rules learned from data."),
                 dict(i="🎬", t="Recommendations", d="Netflix, Spotify and Amazon suggest what you will like."),
                 dict(i="🗺️", t="Maps & arrival times", d="Google Maps predicts traffic and your arrival time."),
                 dict(i="📧", t="Spam filters", d="Outlook decides which emails are junk.")],
                bottom="None of these <b>write</b> anything. They predict, classify or recommend. Writing is one kind of AI — the newest.", cols=3))
add(circles_slide("b1circ", "t1", "Where LLMs fit", "Every LLM is AI. <span class=\"hl\">Not every AI is an LLM.</span>",
                  [("Artificial intelligence", "the whole field — machines doing tasks that need human-like judgement"),
                   ("Machine learning", "learns from data instead of fixed rules — e.g. fraud detection"),
                   ("Deep learning", "large neural networks — e.g. face recognition"),
                   ("Generative AI", "creates new content — text, images, audio"),
                   ("Large language models", "generative AI for language — ChatGPT, Claude, Gemini, the engine in Copilot")],
                  "An LLM is a <b>specialist inside a big family</b>. Your bank's fraud model is AI — but it cannot write an email.",
                  say="Fact: this is correct. LLMs are a type of generative AI, built with deep learning, which is part of machine learning, which is part of AI."))
add(cards_slide("b1llm", "t1", "term", "The kind behind Copilot", "And what is an <span class=\"hl\">LLM?</span>",
                "<b>Large Language Model</b> — a pattern machine trained on huge amounts of text. It writes by predicting the next piece of text.",
                [dict(i="📖", t="Read almost everything", d="Books, websites, code — billions of pages of text."),
                 dict(i="🎯", t="Predicts the next piece", d="It does not look facts up. It continues the pattern."),
                 dict(i="🧊", t="Frozen at training", d="It knows nothing after its training date — and nothing about your clients.")],
                bottom="Examples: <b>GPT</b> (OpenAI · ChatGPT) · <b>Claude</b> (Anthropic) · <b>Gemini</b> (Google) · <b>Llama</b> (Meta). Microsoft 365 Copilot is built on models like these.", cols=3))
add(check(1, 1, "Which one of these is <b>not</b> an LLM?",
          [("The bank's card-fraud detection model", True, "Right. It is AI — machine learning — but it classifies payments. It does not read or write language."),
           ("ChatGPT", False, "ChatGPT runs on GPT, a large language model."),
           ("Claude", False, "Claude is a large language model made by Anthropic.")]))
add(ac_slide("b1auto", "t1", "Block 1 · The human autocomplete", "Shout the <span class=\"hl\">next word.</span>",
             [["The Q3 report is due on", "Thursday"], ["Please find the memo", "attached"], ["Past performance is not a guide to future", "returns"]],
             "That reflex — guessing the most likely next word — <b>is the whole engine.</b>"))
add(cards_slide("b1learn", "t1", "term", "1 of 3 · How it learns", "It remembers the patterns — <span class=\"hl\">not the pages.</span>", None,
                [dict(n="Training", t="Reads billions of sentences", d="It learns which words tend to follow which."),
                 dict(n="Result", t="Fluent about the world", d="Grammar, finance terms, writing styles — all patterns."),
                 dict(n="Limit", t="Knows nothing about your client", d="Until you <b>give it the file</b>, it can only guess.")],
                bottom="Fluent about the world. <b>Knows nothing about Al-Murjan</b> — until you attach the export.", cols=3))
add(tok_slide("b1tok", "t1", "2 of 3 · How it answers", "One piece <span class=\"hl\">at a time.</span>",
              "Ask: “Summarise the Al-Waha portfolio's Q3.” Watch the answer appear piece by piece — each one the most likely next piece.",
              [["The", "92%"], ["Al-Waha", "88%"], ["portfolio", "95%"], ["rose", "61%"], ["1.3%", "54%"], ["in", "97%"], ["Q3,", "90%"], ["led", "47%"], ["by", "96%"], ["technology", "58%"], ["shares.", "71%"]],
              "Each piece is a <b>token</b> — about ¾ of a word. Your prompt <b>steers</b> every pick."))
add(gap_slide("b1gap", "t1", "3 of 3 · Why it makes things up", "Fluent <span class=\"hl\">≠ correct.</span>",
              "Ask about a number it has never seen — with no file attached:",
              "“The Gulf Horizon REIT paid a dividend yield of <mark>6.2%</mark> in Q3, above its five-year average.”",
              "A gap gets filled with a confident guess — a <b>hallucination</b>. No source, no trust."))
add(case(1, "Six cases that <span class=\"hl\">never existed.</span>", 6, "", 0, "Mata v. Avianca · New York · 2023",
         "Two lawyers filed a court brief written with ChatGPT. It cited <b>six court decisions that did not exist</b>. The judge fined them and their firm <b>US$5,000</b>.",
         [(6, "", 0, "Invented court cases"), ("$5,000", "", 0, "Fine"), (2023, "", 0, "Year")],
         "Next: the same engine, wired into your work →"))
add(bridge_slide("b1bridge", "t1", "Block 1 · Bridge", "That's the engine: patterns, tokens, the odd confident guess.",
                 "Now Microsoft wires it into your apps — and points it at <b>your own work</b>. That's Copilot."))
add(cards_slide("b1cop", "t1", "term", "What is Copilot?", "The same engine — <span class=\"hl\">wired into your work.</span>", None,
                [dict(n="Part 1", i="🧩", t="Microsoft 365 apps", d="Outlook, Excel, Word, PowerPoint, Teams — where you already work."),
                 dict(n="Part 2", i="🧭", t="Microsoft Graph", d="Your emails, files, meetings and chats — <b>only what you can already open</b>."),
                 dict(n="Part 3", i="🧠", t="Large language model", d="The engine that reads and writes.")],
                bottom="Press Enter → Copilot gathers your context → the LLM writes → it checks → you get the answer. <b>You own the output.</b>", cols=3))
add(analogy(1, 2, "Think of it like…", "A brilliant new intern — with a badge.",
            "It has read almost everything and works very fast. Its badge opens <b>only the doors yours opens</b>. It needs a clear brief — and your sign-off before anything leaves the building.",
            scene("pass")))
add(demo(1, 2, "Live demo · Work vs Web", "Same question. <span class=\"hl\">Two different worlds.</span>",
         "Click the switch. In Work mode, Copilot answers from the house view in your files. In Web mode, it answers from the internet.",
         chat("Microsoft 365 Copilot Chat", "Signed in with your KAMCO work account", [], toggle=[
             ("work", "Work", [("me", "What is our current view on real estate for client portfolios?", False),
                               ("them", "Your Q4 2026 house view rates real estate as <b>Cautious</b>: do not add, hold existing positions within the mandate range.<br><span class=\"srcchip\">source · house-view-q4-2026.docx</span>", False)]),
             ("web", "Web", [("me", "What is our current view on real estate for client portfolios?", False),
                             ("them", "Many global managers see opportunities in real estate as rates fall, especially in logistics and data centres…<br><span class=\"srcchip\">source · public websites</span>", False)])]),
         bullets=["Toggle Work → Web. Same question, different source.", "Work = KAMCO files you can access. Web = public internet.", "For client work: Work mode, and check the source."],
         say="Run it live in Copilot Chat too if the connection is good."))
add(compare_slide("b1wall", "t1", "Work account vs personal chatbot", "Same kind of engine — <span class=\"hl\">very different walls.</span>",
                  ("Inside · Copilot with your KAMCO account", "Your prompts and files stay inside KAMCO's Microsoft 365 boundary, with enterprise data protection."),
                  ("Outside · a personal or public chatbot", "No KAMCO protection. You do not control where client data goes. Client data never goes here."),
                  [("Grounded", "Answers from your work content when you ask it to."), ("Respects permissions", "Sees only what you can already open."), ("Protected", "Your prompts and data are not used to train the AI models.")]))
add(check(1, 4, "Which of these is fine to use in Copilot with your KAMCO work account?",
          [("A client's civil ID number, “just to check the format”", False, "The task does not need it. Even in a safe tool, share only what the task needs."),
           ("The 30 Sep custody export for a client you manage", True, "Right. Your client, your work file, inside KAMCO's boundary — and the task needs it."),
           ("A confidential pitch book another firm sent you by mistake", False, "You should not be using it at all — with or without AI.")]))
add(case(1, "Three leaks in <span class=\"hl\">twenty days.</span>", 3, "", 0, "Samsung · 2023",
         "Weeks after engineers were allowed to use a public chatbot, staff pasted <b>confidential source code and meeting notes</b> into it. Samsung then <b>banned public generative AI tools</b> on company devices.",
         [(3, "", 0, "Reported leaks"), (20, "", 0, "Days after access"), ("May", "", 0, "2023 · ban announced")],
         "Next: hands-on →", sid="t1case2"))
add(lab_intro("b1lab", "t1", "Hands-on · 15 min", "First contact — <span class=\"hl\">then sort what's safe.</span>",
              [("E1.1", "First contact", "Pick a starter, replace the [brackets], run it in Copilot Chat. Would you use the result?", "5 min"),
               ("E1.2", "Your time audit", "Three tasks that drain your week — tagged Generate, Condense, Find or Transform, with hours.", "5 min"),
               ("E1.3", "Safe or not?", "Five items: fine in work Copilot, fine after removing personal data, or never.", "5 min")],
              "One result you would use. Three tasks audited. Five items sorted.", LAB + "#E1.1", extra="Every task in the lab has a <b>Stretch</b> and a <b>Boss</b> challenge — keep going."))
add(pause(1))
add(break_slide("break1", "t1", 10, "10:30", "Prompting with CTFT"))

# ===================== BLOCK 2 · PROMPTING =====================
add(draw_slide("b2draw", "t2", "Block 2 · Describe the drawing", "Describe it — <span class=\"hl\">no questions allowed.</span>",
               "One volunteer describes a shape. Everyone else draws it blind. No questions.",
               "Vague instructions, vague results. Copilot is the same — except <b>you can keep talking</b>."))
add(cards_slide("b2ctft", "t2", "term", "The recipe", "CTFT — <span class=\"hl\">four ingredients.</span>", None,
                [dict(n="C", t="Context", d="The situation — who you are, who it is for."), dict(n="T", t="Task", d="What to do — one strong verb."),
                 dict(n="F", t="Format", d="The shape — length, bullets, table."), dict(n="T", t="Tone", d="The voice — formal, warm, plain.")],
                bottom="A weak answer = a <b>missing ingredient</b>.", cols=4))
add(ctft_part("b2c", "t2", 1, "C", "Context", "Context — the setup.", "Copilot knows the world — not <b>your</b> situation.",
              "Summarise this portfolio.", "I am the relationship manager for Al-Waha Family Office. The family meets us this week and is worried about property.",
              "Answer:", ["Who am I?", "What is the situation?", "Who is it for?", "Any limits?"]))
add(ctft_part("b2t", "t2", 2, "T", "Task", "Task — the what.", "Name the action.",
              "Help me with this file.", "Using /awfo-q3-custody-export.xlsx, check real estate against the mandate and list any breach.",
              "Strong verbs:", ["Summarise", "Compare", "Check", "Draft", "Rewrite", "List", "Explain"], rule="<b>One main task per prompt.</b>"))
add(ctft_part("b2f", "t2", 3, "F", "Format", "Format — the shape.", "Say nothing, and Copilot picks for you.",
              "Write something for Reem.", "Five bullet points with KWD figures, then one sentence on next steps. Under 120 words.",
              "Specify:", ["Length", "Bullets or table", "Document type", "Units (KWD, %)"]))
add(ctft_part("b2o", "t2", 4, "T", "Tone", "Tone — the voice.", "Same facts, different feel.",
              "Write an email.", "Calm and reassuring, but honest about any breach. Plain English for a family CFO.",
              "Try:", ["Formal", "Warm", "Concise", "Firm", "Plain English"]))
add(cards_slide("b2ms", "t2", "term", "Microsoft's version", "What · why · <span class=\"hl\">which</span> · how.", None,
                [dict(n="Goal", t="What?", d="≈ Task"), dict(n="Context", t="Why? Who?", d="≈ Context"),
                 dict(n="Source", t="Which files?", d="Type <b>/</b> to point at a file, email or meeting."), dict(n="Expectations", t="How?", d="≈ Format + Tone")],
                bottom="Same recipe, new labels. The extra: <b>Source</b> — name the file every time a number matters.", cols=4))
R = [("context", "Khalid Al-Waha, a client for ten years, emailed us upset that Gulf Horizon REIT fell 5% in Q3. He asks why we still hold it."),
     ("task", "Write a reply that explains the fall in plain terms and says what we will review at our next meeting."),
     ("format", "Under 120 words, three short paragraphs, with my direct number at the end."),
     ("tone & limits", "Warm and respectful. Do not promise the price will recover, and do not mention other clients.")]
add(standby("b2hero", "Hero exercise · E1.3 · 15 min", "From zero to <span class=\"hl\">hero.</span>",
            "One weak prompt. Four rounds. Watch it get visibly better — run each round in Copilot Chat with us.",
            ["<b>Scenario:</b> a long-standing client is upset that a REIT in his portfolio fell 5% in Q3.", "Round 0 is mush. Round 4 is sendable."], None, t="t2", k="demo"))
add(round_slide("b2r0", "t2", "Round 0 · the weak prompt", "Watch it be <span class=\"hl\">generic.</span>", "Run this — together.",
                [("", "Write an email to a client.", True)], 8, "mush"))
for i, (lab, txt) in enumerate(R, 1):
    parts = [(R[j][0], R[j][1], j == i - 1) for j in range(i)]
    q = [32, 55, 76, 95][i - 1]; v = ["no task, so it guesses", "right content, wrong shape", "usable", "sendable"][i - 1]
    add(round_slide("b2r%d" % i, "t2", "Round %d · + %s" % (i, lab.title()), ["Give it <span class=\"hl\">the situation.</span>", "Say <span class=\"hl\">what to do.</span>", "<span class=\"hl\">Shape</span> it.", "Set the voice — <span class=\"hl\">and the limits.</span>"][i - 1],
                    "Add the highlighted part and run it again.", parts, q, v))
add(cards_slide("b2ins", "t2", "close", "The insight", "Nobody nails it in one shot — <span class=\"hl\">that's the method.</span>", None,
                [dict(i="🔁", t="Iterate, don't restart", d="Short follow-ups in the same chat: <b>“shorter”</b> · <b>“warmer”</b> · <b>“in Arabic”</b> · <b>“KWD only”</b>."),
                 dict(i="📎", t="Name the source", d="“Use <b>/awfo-q3-custody-export.xlsx</b>” beats “use the latest numbers”."),
                 dict(i="✅", t="Check before you use", d="Every number traced back to the file.")], cols=3))
add(check(2, 4, "Copilot's summary used the old June factsheet. What is your best next step?",
          [("Start a new chat and type everything again", False, "You lose the context you already built. Correct it in the same chat."),
           ("Reply: “Use only /awfo-q3-custody-export.xlsx (30 Sep). Redo the summary.”", True, "Right. Iterate in the same chat and name the exact source."),
           ("Fix the numbers by hand inside Copilot's answer", False, "Slow and risky — the rest of the answer may still use the old file.")]))
add(case(2, "Grounded in the firm's <span class=\"hl\">own research.</span>", 98, "%", 0, "Morgan Stanley Wealth Management · 2023–24",
         "Morgan Stanley gave its financial advisers an AI assistant that answers from the firm's <b>own research library</b>. Reported adoption reached about <b>98% of advisor teams</b>. The value came from <b>good sources and clear questions</b>.",
         [("100k", "", 0, "Research documents, approx."), (2023, "", 0, "Year launched"), (98, "%", 0, "Advisor teams using it")], "Next: hands-on →"))
add(lab_intro("b2lab", "t2", "Hands-on · 20 min", "From zero to hero — <span class=\"hl\">then build your own.</span>",
              [("E1.4", "From zero to hero", "One weak client email, four rounds. Add one CTFT ingredient each round and rate the result 1–5.", "10 min"),
               ("E1.5", "Build your own prompt", "Pick a task from your time audit. Build a CTFT prompt in the builder and run it in Copilot Chat.", "10 min")],
              "Five ratings, one prompt you will reuse. Best one = <b>Prompt of the Day</b>.", LAB + "#E1.4", extra="Fill the Example field in the builder and run it again — one example changes the structure and voice."))
add(pause(2))
add(break_slide("break2", "t2", 10, "11:30", "Read the request in Outlook"))

# ===================== BLOCK 3 · OUTLOOK =====================
add(story(3, "Block 3 · Read the request in Outlook", "The buried deadline",
          "The first email says Thursday. Two emails later, the client moves the meeting and the deadline becomes <b>Monday, 1:00 pm</b>. You read the first email only. You deliver on Thursday. <b>The meeting already happened.</b>",
          "The real ask is often in the <span class=\"hl\">newest message.</span>"))
add(term(3, 1, "This is <span class=\"hl\">Summarise by Copilot.</span>", "SUMMARISE (OUTLOOK)",
         "At the top of an email thread in Outlook, click <b>Summarise</b>. Copilot reads every message and lists the key points, with links back to the source message.",
         "Like a chief of staff's one-pager, it gives you <b>the whole thread fast</b>…", "but you still open <b>the newest message</b> to check what changed."))
waha_body = ('<p><b>Sun 11 Oct · Reem:</b> Update: the family wants ' + hot("a short memo only - no slides this time", True, "The deliverable changed. A memo, not a deck.")
             + '. Please send it to me by ' + hot("Monday 12 Oct, 1:00 pm", True, "The real deadline, from the newest message.")
             + '.</p><p>They are worried about property. Please ' + hot("check real estate against the mandate first", True, "The priority: real estate first.")
             + ', then the rest of the allocation, and ' + hot("the 10% issuer limit", True, "A required check: no issuer above 10%.") + '.</p><p>Use ' + hot("the 30 Sep custody export attached", True, "The right source — not an older file.") + '.</p>'
             + '<div class="mail-sep">Wed 7 Oct · earlier message</div><p>Please prepare ' + hot("a 4-slide deck", False, "Old request — replaced by 'memo only'.")
             + ' with the Q3 value, the Q3 change, allocation against the mandate and the top contributors. I need it by ' + hot("Thursday 15 Oct", False, "Old deadline — replaced by Monday 1:00 pm.") + '.</p>')
add(demo(3, 1, "Live demo · find the ask", "Five things matter. <span class=\"hl\">Two are traps.</span>",
         "Click the parts of the thread that define the job. Old instructions do not count.",
         mailbox("Outlook · thread (2 messages)", "Reem Al-Qattan (Head of Client Advisory)", "You", WAHA_THREAD["subject"], waha_body, attach=WAHA_THREAD["attach"])
         + '<div class="foundct">Found <b>0</b> / 5</div><div class="mini-note hotnote" data-def="Tip: start with the newest message."></div>'
         + '<div class="keyline hotwin" style="display:none">All five. <b>Memo only, Monday 1:00 pm, real estate first, issuer limit, 30 Sep file.</b> Now compare with Copilot&rsquo;s summary.</div>',
         bullets=["Find the 5: memo only · Mon 12 Oct 1:00 pm · real estate first · 10% issuer limit · 30 Sep export.", "Traps: '4-slide deck' and 'Thursday 15 Oct' are old.", "Then click Summarise in Outlook live and compare."]))
add(demo(3, 2, "Live in Outlook · two prompts", "Thread → <span class=\"hl\">checklist → holding reply.</span>",
         "Open the thread, then use Copilot. The second prompt gives the sender a quick answer while you work.",
         prompts([("Copilot in Outlook · on the thread", "From this thread, list in a table: 1) the final deadline, 2) each deliverable and its format, 3) who must be copied, 4) any request I should NOT do, and why. Use the newest message when instructions change.", "Deadline and deliverable match the newest message."),
                  ("Copilot in Outlook · Draft with Copilot", "Draft a short reply to Reem: confirm I will send the memo by Monday 12 Oct, 1:00 pm, and that I will check real estate first. Under 60 words, professional.", "Then use Coaching by Copilot to check tone and clarity before sending.")]),
         bullets=["Run prompt 1 on the Al-Waha thread.", "Run prompt 2 with Draft with Copilot.", "Show Coaching by Copilot on the draft."]))
add(check(3, 3, "Copilot's summary says the deadline is “Thursday 15 Oct”. What happened?",
          [("Nothing — summaries are always right", False, "Summaries can mix old and new instructions. You check the newest message."),
           ("It picked up the old instruction. The newest message says Monday 12 Oct, 1:00 pm", True, "Right. Always check dates against the newest message before you plan your day."),
           ("Reem made a mistake — ask her to resend", False, "The thread is clear. The newest message changed the deadline.")]))
add(check(3, 4, "A client asks you to send another family's report “so we can see your format”. What do you do?",
          [("Send it — they are a client too", False, "That shares one client's private data with another. Never."),
           ("Send it with the names removed", False, "Holdings and values can still identify a family. Do not share another client's report."),
           ("Do not send it. Offer a blank sample of the format instead", True, "Right. Another client's data never leaves. A blank sample shows the format safely.")]))
add(lab_intro("b3lab", "t3", "Hands-on · 15 min", "Tame the thread — <span class=\"hl\">then reply.</span>",
              [("E1.6", "Tame the thread — then reply", "Summarise Faisal's thread, find the real deadline and asks, draft the reply, check it before sending.", "15 min")],
              "The newest deadline found. One request politely declined. A reply you would send.", LAB + "#E1.6", extra="Ask Copilot what the client will ask about on Wednesday that the thread does not cover."))
add(break_slide("break3", "t3", 60, "13:00", "Excel · clean the data", label="Lunch · 60 min"))

# ===================== BLOCK 4 · EXCEL CLEAN =====================
add(standby("b4up", "Block 4 · Quick stand-up", "One sentence: the best thing <span class=\"hl\">Copilot</span> did for you this morning.",
            "Two or three voices — then straight in.", [], None, t="t4", k="story"))
add(story(4, "Block 4 · Excel: clean the data", "The double-counted bond",
          f"The Al-Waha custody export lists three holdings twice. Nobody notices. The total comes out at <b>{kwd(W['wrong_if_dups_kept'])}</b>. The real value is <b>{kwd(W['total_sep'])}</b>. The family sees a portfolio <b>{(W['wrong_if_dups_kept']/W['total_sep']-1)*100:.0f}% bigger</b> than it is.",
          "Clean first. <span class=\"hl\">Count second.</span>"))
add(term(4, 1, "This is <span class=\"hl\">data cleaning.</span>", "DATA CLEANING",
         "Removing duplicates, turning text into numbers, filling missing values from a trusted source, and making labels consistent — <b>before</b> any formula or total.",
         "Like a chef's preparation before service, it happens <b>first</b>…", "a total is only as good as the rows under it."))
rows = [("AWFO-0107", "Najd Industrial Holding", "22000", "17.25", 0, ""), ("AWFO-0116", "US Treasury Note 2030", "'8,800'", "96.75", 1, "Quantity stored as text — Excel will not add it."),
        ("AWFO-0111", "Crestview Consumer", "'4,100'", "—", 1, "Price is missing — fill it from the Price_List sheet."),
        ("AWFO-0102", "Gulf Trade Bank", "1000000", "0.498", 0, ""), ("AWFO-0112", "Harbor Semiconductors", "3100", "101.90", 0, ""),
        ("AWFO-0114", "Al-Noor Bank Sukuk 2029", "1500", "99.60", 0, ""), ("AWFO-0103", "Bayan Telecom", "540000", "0.471", 0, ""),
        ("AWFO-0103", "Bayan Telecom", "540000", "0.471", 1, "Duplicate — same Holding ID as a row above."),
        ("AWFO-0112", "Harbor Semiconductors", "3100", "101.90", 1, "Duplicate — same Holding ID as a row above.")]
tbl = ('<div class="mini" style="padding:0;overflow:auto"><table class="logtable"><tr class="logrow head"><th>Holding ID</th><th>Security</th><th>Quantity</th><th>Price 30-Sep</th></tr>'
       + "".join(f'<tr class="logrow" data-bad="{b}"><td>{i}</td><td>{s}<span class="why">{w}</span></td><td class="num">{q}</td><td class="num">{p}</td></tr>' for i, s, q, p, b, w in rows)
       + '</table></div><div class="foundct">Problems found <b>0</b> / 4</div><div class="keyline hotwin" style="display:none">Four problems in nine rows. <b>Now imagine 2,000 rows</b> — that is why we ask Copilot to find them, then we check.</div>')
add(demo(4, 1, "Live demo · spot the problems", "Nine rows from the export. <span class=\"hl\">Four will hurt you.</span>", "Click every row that would make a total wrong.", tbl,
         bullets=["Problems: text quantity (UST30), missing price (CVC), duplicate Bayan Telecom, duplicate Harbor.", "Clean rows go grey when clicked."]))
add(term(4, 2, "This is <span class=\"hl\">Copilot in Excel.</span>", "COPILOT IN EXCEL",
         "Works on files saved in <b>OneDrive or SharePoint</b> with AutoSave on, and works best when the data is a <b>table</b> (Ctrl+T). It can highlight, sort, filter, add formula columns and explain its formulas.",
         "Like a colleague tidying your file, it works <b>fast</b>…", "and you check <b>what it changed</b>.",
         "Before: delete the title rows above the headers, then <b>Ctrl+T</b>."))
add(demo(4, 2, "Live in Excel · clean the Al-Waha export", "Five prompts. <span class=\"hl\">Check after each one.</span>",
         "Delete rows 1–3 above the headers, format as a table (Ctrl+T), then run these in order.",
         prompts([("Copilot in Excel", "Highlight duplicate rows in this table based on Holding ID.", "Three duplicates: Bayan Telecom, Harbor Semiconductors, Gulf Sovereign. Then remove them (Data › Remove Duplicates)."),
                  ("Copilot in Excel", "Convert the Quantity column to numbers. Some values are stored as text with commas.", "All quantities right-aligned. Row count after removing duplicates: 22."),
                  ("Copilot in Excel", "Add a column called Asset Class (clean) that maps equities, EQ and Equity to Equity; FI, Bonds and fixed income to Fixed Income; REIT to Real Estate; Cash & Deposits and cash to Cash.", "Only four values in the new column."),
                  ("Copilot in Excel", "Add a column called Price 30 Sep (filled). Use Price 30-Sep-2026. If it is blank, look up the Ticker in the Price_List sheet. Trim spaces from the Ticker first.", "The two blanks (CVC, SPF) now have prices."),
                  ("Copilot in Excel", "Add a column Market Value KWD = Quantity × Price 30 Sep (filled) × the rate to KWD from the FX_Rates sheet (USD = 0.3065, KWD = 1). Show me the formula.", f"Total should be {kwd(W['total_sep'])}.")]),
         bullets=["Run live on the Al-Waha file.", f"Before/after: 25 rows → 22 rows. Total {kwd(W['total_sep'])}.", "Ask Copilot to show each formula. Test one row by hand."]))
add(check(4, 3, "Copilot says it “removed duplicates”. The rows drop from 25 to 21. You expected 22. What next?",
          [("Accept it — Copilot knows the data", False, "One row too many disappeared. That is a real holding gone from the total."),
           ("Ask which rows it removed, and compare the Holding IDs", True, "Right. Check what changed. A real holding may have been removed because it looked similar."),
           ("Undo everything and clean by hand", False, "You do not need to give up — find and fix the one wrong removal.")]))
add(case(4, "One spreadsheet range. <span class=\"hl\">A global debate.</span>", 5, "", 0, "Reinhart & Rogoff · 2010–2013",
         "An influential paper on government debt and growth used an Excel range that <b>left out five countries</b>. A graduate student found it in 2013. With the error fixed, the headline result <b>changed sharply</b>.",
         [(5, "", 0, "Countries left out"), (90, "%", 0, "Debt threshold in the paper"), (2013, "", 0, "Error found")], "Next: hands-on →"))
add(lab_intro("b4lab", "t4", "Hands-on · 15 min", "Clean the <span class=\"hl\">Al-Murjan export.</span>",
              [("E1.7", "Clean the export", "Same five prompts on your file. Record raw rows, duplicates removed, holdings left, missing prices.", "15 min")],
              "Row count checked before and after every step.", LAB + "#E1.7", extra="Ask Copilot which columns still have inconsistent values, then make every Price Date a real date."))
add(pause(4))
add(break_slide("break4", "t4", 10, "14:00", "Excel · find the story"))

# ===================== BLOCK 5 · EXCEL STORY =====================
add(bridge_slide("b5bridge", "t5", "Block 5 · Find the story", "The family CFO does not want 22 rows.",
                 "He asks one question: <b>“Are we still inside the mandate?”</b> Your analysis must answer it in one line — and prove it."))
add(term(5, 1, "This is a <span class=\"hl\">PivotTable.</span>", "PIVOTTABLE",
         "A summary that groups rows by a category — like asset class or issuer — and totals them. Copilot can build one from a prompt.",
         "Like an X-ray instead of a photo album, it shows <b>the shape</b>…", "allocation by asset class, in seconds."))
alloc = W["alloc_pct"]
bars = '<div class="bars">' + "".join(
    f'<div class="bar-row{" over" if not (MANDATE[a][1]*100 <= alloc[a] <= MANDATE[a][2]*100) else ""}"><div class="bn">{a}</div><div class="bar-track"><div class="bar-band" style="left:{MANDATE[a][1]*100/0.7:.1f}%;width:{(MANDATE[a][2]-MANDATE[a][1])*100/0.7:.1f}%"></div><div class="bar-fill" style="width:{alloc[a]/0.7:.1f}%"></div></div><div class="bv">{alloc[a]:.1f}%</div></div>'
    for a in MANDATE) + '<div class="bar-legend">Bar = weight at 30 Sep · shaded band = mandate range (min–max) · scale 0–70%</div></div>'
bars += '<div class="demo-controls"><button class="btn bars-check">Check against the mandate →</button></div><div class="keyline bars-note" style="display:none">Real estate is <b>4.5%</b> — below the 5% minimum. Equity at 54.4% is inside, but close to the 55% maximum. <b>That is your first line to Reem.</b></div>'
add(demo(5, 1, "Live demo · allocation vs mandate · Al-Waha", "Inside the range — <span class=\"hl\">or not?</span>",
         "The weights come from the cleaned Al-Waha file. Click to compare each one with its range.", bars,
         bullets=["Click 'Check against the mandate'.", "Real estate 4.5% < 5% minimum → breach.", "Equity 54.4% inside but close to 55%."]))
add(term(5, 2, "This is a <span class=\"hl\">mandate check.</span>", "MANDATE CHECK",
         "Compare each asset-class weight with its minimum and maximum. Then add up every holding from the <b>same issuer</b> — shares and bonds together — and compare with the 10% limit.",
         "Like a bridge's weight limit, it counts <b>the whole truck</b>…", "equity <b>and</b> bonds from one name count together."))
add(demo(5, 2, "Live in Excel · three prompts", "Allocation, issuers, <span class=\"hl\">movers.</span>",
         "Run on the cleaned Al-Waha table. After each answer, ask Copilot to show the formula.",
         prompts([("Copilot in Excel", "Create a PivotTable of Market Value KWD by Asset Class (clean), with each value as a % of the grand total. Add the Min and Max from the Mandate sheet and a column that says BREACH if the weight is outside the range.", "Real estate 4.5% → BREACH (below 5%)."),
                  ("Copilot in Excel", "Sum Market Value KWD by Issuer, excluding cash. Show each issuer as a % of the total portfolio value, sorted from largest to smallest. Highlight any issuer above 10%.", "Gulf Trade Bank 11.75% → above the limit."),
                  ("Copilot in Excel", "Add a column Q3 Change KWD = Quantity × (Price 30 Sep (filled) − Price 30-Jun-2026) × rate to KWD. Show the top 3 and bottom 3 holdings by Q3 Change KWD.", "Top: Atlas Tech Corp. Bottom: Gulf Trade Bank.")]),
         bullets=["Run all three live.", "Issuer: Gulf Trade Bank 11.75% — breach.", f"Top Atlas Tech (+{W['top3'][0][1]:,}); bottom Gulf Trade Bank ({W['bottom3'][0][1]:,})."]))
add(verify_slide("b5vfy", "t5", "The verify habit", "It summarises beautifully — <span class=\"hl\">and still misses a piece.</span>",
                 "“Meridian Energy is <mark>2.6%</mark> of the Al-Waha portfolio — well inside the issuer limit.”",
                 "2.6% is the <b>shares only</b>. Add the Meridian Energy 5.1% 2032 bond: <b>8.0%</b> of the portfolio. Still inside 10% — but now you know why.",
                 "Ask: <b>“Show me which rows you added up.”</b> Then check them yourself."))
add(check(5, 4, f"Copilot says the Al-Waha Q3 return is 3.1%. Your table shows {W['q3_return_pct']}%. Which do you use?",
          [("Copilot's — it calculated it", False, "Two different numbers means one is wrong. Find out which before either goes anywhere."),
           ("Ask Copilot for its formula, and test one row by hand", True, "Right. Often it used the wrong column or kept the duplicates. You can only send a number you can explain."),
           ("Average the two", False, "Averaging two numbers, one of them wrong, gives you a third wrong number.")]))
add(case(5, "A copy-paste error inside <span class=\"hl\">a risk model.</span>", "$6.2B", "", 0, "JPMorgan “London Whale” · 2012",
         "A risk model built in spreadsheets had manual copy-paste steps and a formula error that <b>understated risk</b>. The trading losses reached about <b>US$6.2 billion</b>. JPMorgan's own review named the spreadsheet process.",
         [("$6.2B", "", 0, "Trading losses"), (2012, "", 0, "Year"), ("Excel", "", 0, "Where the error lived")], "Next: hands-on →"))
add(lab_intro("b5lab", "t5", "Hands-on · 20 min", "Value, mandate, <span class=\"hl\">issuers.</span>",
              [("E1.8", "Value and mandate", "Total value, Q3 change, equity weight — and which asset class is outside its range.", "10 min"),
               ("E1.9", "Issuers and movers", "Largest issuer and its weight; top and bottom contributors.", "10 min")],
              "Every number explained — and checked against your tables.", LAB + "#E1.8", extra="Ask Copilot how much Al-Noor Bank must be sold to get back to 10% — and check its maths by hand."))
add(pause(5))
add(break_slide("break5", "t5", 10, "15:00", "Hands-on · the Al-Murjan request, alone"))

# ===================== HANDS-ON · RECAP · CLOSE =====================
add(standby("hands", "Hands-on · 50 minutes", "Your turn: <span class=\"hl\">Al-Murjan, alone.</span>",
            "You have the thread and the 30 Sep export. Take the request from the email to a clean, checked analysis.",
            ["Finish the <b>Day 1 lab</b> tasks you have not marked done — then try the Stretch and Boss challenges.",
             "In your Excel file: value at 30 Sep, Q3 change, allocation vs mandate, issuer check, top 3 and bottom 3.",
             "Ask Copilot to write <b>three findings</b> in one line each — then check every number against your table.",
             "<b>Save your file in OneDrive.</b> You need it tomorrow.",
             "<b>Finished early?</b> Draft the three findings as a 60-word holding reply to Faisal in Outlook — and run Coaching by Copilot on it."],
            "50 minutes · instructors are watching how you work", t="close", k="demo",
            say="Evidence for the evaluation. Watch for: cleaning before counting, checking formulas, and the confidentiality trap in Khalid's email."))
add(recap_slide("recap", "Day 1 · Recap · the callback lap", "Look at <span class=\"hl\">the wall.</span>", "tasks",
                ["Which of these tasks could Copilot help with now — and how?", "<b>Prompt of the Day</b> — steal it.", "One line each: “The one thing I will use tomorrow is…”"]))
add(close("Day 1 · done", "Request → <span class=\"hl\">Check.</span>",
          "You found the real ask in a messy thread, cleaned a custody export, and checked a portfolio against its mandate — with every number explained. <b>Tomorrow: Word, PowerPoint and the reply.</b>",
          "Bring your Al-Murjan file tomorrow"))
