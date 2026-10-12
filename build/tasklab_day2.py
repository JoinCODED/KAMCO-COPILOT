"""Day 2 trainee lab — task format (MCIM lab engine). Word, PowerPoint, Prompt Library, Agents, Safe use, graded project."""
import emails
from tasklab_day1 import build, COP

THREAD = emails.thread_text(emails.MURJAN_THREAD)
HV = [{"label": "house-view-q4-2026.docx · Investment House View Q4 2026", "href": "house-view-q4-2026.docx",
       "note": "Save it to your <b>OneDrive</b> first — Copilot can only point at files it can reach. Type <kbd>/</kbd> in the Copilot box to pick it."}]
NOTES = """AL-MURJAN FAMILY OFFICE - Q3 REVIEW PREP - meeting notes   [training sample]
Sun 11 Oct 2026 - Faisal Al-Mutairi, you, Noura (Compliance)

- Client meeting with Khalid (CFO) moved to Wed 14 Oct, 11:00. Pack due to Faisal Tue 13 Oct, 3:00 pm.
- Portfolio value at 30 Sep: KWD 4,696,424. Q3 change +KWD 112,674 (+2.46%).
- Equity 61.0% vs mandate max 55% -> breach after the Q3 rally (Atlas Tech, Al-Noor Bank, Harbor Semiconductors).
- Al-Noor Bank shares + sukuk = 12.21% of the portfolio -> above the 10% issuer limit. Trim about KWD 104k to get back under.
- Fixed income 22.8% (range 20-40%). House view is positive on fixed income - room to add.
- Real estate 8.3%, cash 7.9% - both inside their ranges.
- Khalid asked for the Al-Rumaithiya family report as a format example -> NO, another client's data. Offer a blank template instead.
- Noura: copy Compliance on anything that goes to the client. Disclaimer on client documents only.
- Decisions for Faisal: (1) propose trimming equities back inside 55%, (2) trim Al-Noor Bank below 10%, (3) where to put the proceeds - fixed income, in line with the house view."""

TASKS = [
 dict(id="E2.1", app="Word", title="Notes in — a memo out", minutes="20 min", block="Block 1 · Word", writeOwn=True,
      scenario="Yesterday's prep meeting for the Al-Murjan review ran long. Your notes are below. Faisal wants <b>one page</b> before 10:00: where we stand, what is outside the rules, and the decisions he must make.",
      steps=["Copy your notes (tap the box below). In Word, open a <b>new blank document</b> and select <b>Copilot</b> (or <b>Draft with Copilot</b>).",
             "<b>Draft:</b> write your prompt for goal 1 and paste your notes after it. Read the result once. Don't fix anything by hand yet.",
             "<b>Rewrite:</b> write your prompt for goal 2. Steer it — don't retype.",
             "<b>Ground:</b> save the house view (below) to your OneDrive. Write your prompt for goal 3 and pick the file after you type <kbd>/</kbd>. No file option? Upload or paste the file's text instead.",
             "<b>Check:</b> compare the final version with your notes. Anything missing? Anything invented? Fix it by hand."],
      fallback="Open Copilot Chat. Paste your notes and write your prompts for the same goals. For goal 3, upload the house view with <b>+</b> → <b>Upload</b>. Copy the final text into Word.",
      briefs=[{"label": "Your notes · Al-Murjan Q3 review prep", "text": NOTES}], files=HV,
      prompts=[{"label": "1 · Draft", "goal": "Turn your notes into a one-page internal memo to Faisal: where we stand, what is outside the rules, and the decisions he must make.",
                "text": "Using these notes, draft a one-page internal memo to Faisal Al-Mutairi, Managing Director, Wealth Management. Three sections: Where we stand, What is outside the rules, Decisions needed. Under 300 words. [paste the notes]"},
               {"label": "2 · Rewrite", "goal": "Make it shorter. Put the three decisions first, each with a one-line reason.",
                "text": "Make it 20% shorter. Put the three decisions first, each with a one-line reason. Keep every number."},
               {"label": "3 · Ground", "goal": "Match the house view: use its wording for the asset class views and the issuer rule, and follow its number format.",
                "text": "Check this memo against /house-view-q4-2026. Use its wording for the asset class views and the issuer rule. Show KWD values without decimals and percentages to one decimal place."}],
      findings=[{"label": "One thing Copilot changed, dropped or invented — and your fix", "hint": "e.g. it wrote Wednesday as the deadline"}],
      reveal="<ul><li>Deadline: <b>Tue 13 Oct, 3:00 pm</b>; meeting <b>Wed 14 Oct, 11:00</b>.</li><li>House view number format: <b>2.5%</b> (not 2.46%), <b>12.2%</b> (not 12.21%), KWD without decimals.</li><li>Equities are <b>Neutral</b> in the house view (trim back to range); fixed income is <b>Positive</b>.</li><li>Internal memo: <b>no client disclaimer</b> needed. The Al-Rumaithiya report is <b>not</b> an action — it is declined.</li></ul>",
      expect="A one-page memo with the decisions first, every number matching your notes, in the house view's wording and format.",
      stretch="Ask Copilot for a three-line version for Khalid, the client. What must change? (Hint: section 4 and 5 of the house view — client documents need the disclaimer.)",
      boss="Ask: <i>“Which sentence in this memo would Compliance question first, and why?”</i> Fix it."),
 dict(id="E2.2", app="PowerPoint", title="A document becomes a deck", minutes="18 min", block="Block 2 · PowerPoint", writeOwn=True,
      scenario="The trustees of a family office meet tomorrow. Turn the Q4 house view into a <b>6-slide client deck</b> — then check that every statement survived the trip.",
      steps=["Download the house view (below) and save it to your <b>OneDrive</b>.",
             "In PowerPoint, open a <b>blank presentation</b>. Select <b>Copilot</b> → <b>Create a presentation from a file</b> — or type <kbd>/</kbd> in the Copilot box and pick the file. Write your prompt for goal 1.",
             "<b>Generate:</b> write your prompt for goal 2 to add one new slide.",
             "<b>Check:</b> open two slides. Check every statement against the source. Then fix one slide by hand — feel where Copilot stops and you start."],
      fallback="Upload the file to Copilot Chat and run: <i>“Turn this document into a slide-by-slide outline: a title, three bullets and speaker notes for each slide.”</i> Build the slides in PowerPoint from the outline.",
      files=HV,
      prompts=[{"label": "1 · Create", "goal": "A 6-slide client deck from the house view: the view in one line, each asset class, the concentration rule, what it means for a balanced portfolio, next steps — and the standard disclaimer on the last slide. Speaker notes on every slide.",
                "text": "Create a 6-slide client presentation from /house-view-q4-2026: our view in one line, the view on each asset class, the concentration rule, what it means for a balanced portfolio, next steps, and the standard disclaimer on the last slide. Keep every statement traceable to the source. Add speaker notes."},
               {"label": "2 · Generate", "goal": "Add one slide with a simple table: asset class, our view, what we will do in portfolios.",
                "text": "Add one slide with a table of the four asset classes: our view (Positive, Neutral or Cautious) and what we will do in client portfolios. One short line per row."}],
      findings=[{"label": "A statement you checked — and where it is in the source", "hint": "e.g. Real Estate: Cautious · section 2"}, {"label": "Anything wrong, vague or missing?", "hint": "what you fixed by hand"}],
      reveal="<ul><li>Views: Equity <b>Neutral</b> · Fixed Income <b>Positive</b> · Real Estate <b>Cautious</b> · Cash <b>Neutral</b> (keep 5–10%).</li><li>Concentration: no issuer above <b>10%</b>; shares and bonds of the same issuer count <b>together</b>.</li><li>Client deck: the <b>standard disclaimer</b> on the last slide, no promised returns, no other client's name.</li></ul>",
      expect="A 6-slide deck from the house view, one new table slide, and two slides checked line by line.",
      stretch="Ask Copilot to rewrite the deck for the relationship managers instead of the client. What changes — the words, the detail, the disclaimer?",
      boss="Ask: <i>“Which slide would a trustee challenge first, and why?”</i> Add one speaker-note line that answers it."),
 dict(id="E2.3", app="PowerPoint", title="Titles that say the message", minutes="stretch · 7 min", block="Block 2 · PowerPoint", optional=True,
      scenario="Most slide titles name the topic: <i>“Equities”</i>. A busy trustee reads only the titles. Make every title say the <b>message</b> — then cut the deck to three slides.",
      steps=["Read only the titles of your E2.2 deck, top to bottom. Do they tell the story on their own?", "Write your own CTFT prompt for the goal. Run it and compare.", "Then ask for a three-slide version. What survives is the real message."],
      goal="Rewrite every slide title as a full-sentence message (the “so what”), keep the body as it is, and list the old and new titles side by side.",
      prompt="Rewrite every slide title as the message, not the topic — a short full sentence a trustee could read on its own. For example: “Equities: back inside the range after a strong Q3”, not “Equities”. Keep the slide bodies as they are. Then list the old and new titles side by side.",
      hidePrompt=True,
      findings=[{"label": "Your best new title", "hint": ""}, {"label": "The three slides you kept", "hint": ""}],
      expect="Titles that tell the story on their own — and a three-slide version with nothing important lost."),
 dict(id="E2.4", app="Scheduled prompts", title="Schedule a prompt", minutes="5 min", block="Block 3 · Prompts",
      scenario="Some questions you ask every week: <i>what came in from clients, what does Compliance need, which meetings need a pack?</i> Schedule the prompt once and Copilot runs it for you — the answer is waiting when you arrive.",
      steps=[f"Open Copilot Chat ({COP} → Chat, or the Copilot icon in Teams or Outlook).",
             "Pick one prompt below (or write your own with CTFT). Run it <b>once</b> and check the answer is what you want.",
             "Hover over your prompt and select <b>Schedule this prompt</b>. Choose <b>when</b> it runs (for example Sunday 7:30), <b>how many times</b>, and turn on the <b>email notification</b>. Select <b>Save</b>.",
             "Test it: select <b>…</b> (Copilot chats and more) → <b>Scheduled prompts</b> → <b>Run now</b>. The result appears in your chat list on the left.",
             "Not needed after today? Turn it off or delete it from the same page — you can have up to ten."],
      prompts=[{"label": "Sunday 7:30 · the week's inbox", "text": "I look after family-office clients at an investment company. Summarise the emails I received since Thursday from clients and from Compliance. A table: who, the ask, the deadline — urgent first. Short and plain."},
               {"label": "Thursday 14:00 · next week's meetings", "text": "List my client meetings next week. For each one: the client, the date and time, the last email thread with them, and any open action I owe them. A table, earliest first."},
               {"label": "Daily 8:00 · market headlines", "text": "Give me five headlines from the last 24 hours on GCC banks, GCC real estate and oil prices, with a one-line 'why it matters' for each and the source link. No predictions."}],
      fallback="No <b>Schedule this prompt</b> option? Your administrator may have turned off connected experiences — that is normal. Save the prompt in your Word prompt library (E2.6) and run it by hand each week instead.",
      findings=[{"label": "Your scheduled prompt — when it runs and how many times", "hint": "e.g. Sundays 7:30, 4 runs"}, {"label": "What did Run now give you?", "hint": ""}],
      expect="One prompt scheduled on a repeat question about new information — and tested once with <b>Run now</b>.",
      stretch="Schedule a second prompt for Thursday afternoon that prepares you for next week. What would you want to read before the weekend?",
      boss="Make a scheduled prompt that checks for a risk, not just a summary: for example, any client email this week that mentions a deadline, a complaint or a request for another client's information."),
 dict(id="E2.5", app="Prompt Gallery", title="Library hunt", minutes="10 min", block="Block 3 · Prompts",
      scenario="Your prompt library is already built in: Copilot calls it the <b>Prompt Gallery</b>. Microsoft publishes thousands of ready-made prompts there. Find three for your role, adapt one with CTFT, run it, and save it.",
      launch={"href": "https://adoption.microsoft.com/en-us/copilot/prompt-gallery/", "ext": True, "label": "Open the Copilot Prompt Gallery (web)", "note": "Filter by role, app and task · or use the gallery inside Copilot Chat"},
      steps=["Open the Prompt Gallery: inside Copilot Chat (the prompt ideas under the chat box, or the <b>…</b> menu) — or the web version above.",
             "Filter by <b>your role</b> (for example Finance or Sales) and one app. Pick three prompts you would really use.",
             "Adapt one with CTFT: add your context, the format and the tone. Use the example below as a model. Run it in Copilot.",
             "Save it to <b>Your prompts</b> in Copilot."],
      prompts=[{"label": "Typical library prompt", "text": "Summarise my recent emails and list the actions I need to take."},
               {"label": "Adapted with CTFT", "text": "I'm back after three days off and I look after twelve family-office clients. Summarise my emails since Sunday and list the actions I must take. A table: action, client, who asked, deadline — urgent first. Short and plain."}],
      expect="Three library prompts found, one adapted with CTFT, tested, and saved in Copilot.",
      stretch="Share your adapted prompt with a colleague in the room. Did it work for their job without changes — or did they need to change the Context?",
      boss="Find a library prompt for Excel or PowerPoint that would have saved you time yesterday. Adapt it for the Al-Murjan pack."),
 dict(id="E2.6", app="Word", title="Your prompt library in Word", minutes="7 min", block="Block 3 · Prompts",
      scenario="The Gallery is Microsoft's library. Now build <b>yours</b>: one Word file in your OneDrive with the prompts that worked for you on Day 1 and today. Next week, you reuse them in seconds — Copilot can read the file when you type <kbd>/</kbd>.",
      files=[{"label": "my-prompt-library.docx · template with five KAMCO prompts", "href": "my-prompt-library.docx",
              "note": "Download it, then save it to your <b>OneDrive</b> as <b>My Prompt Library</b>. Copilot can only point at files it can reach."}],
      steps=["Download the template (above) and save it to your OneDrive as <b>My Prompt Library</b>. Open it in Word.",
             "Add <b>three prompts of your own</b> that worked on Day 1 or today — from the lab, your E2.4 prompt, or your own job. One row each: name, app, when you use it, the prompt, tested?",
             "Make each prompt reusable: put <b>[brackets]</b> where the details change, and remove client names and numbers.",
             "<b>Reuse it:</b> open Copilot Chat, type <kbd>/</kbd>, pick <b>My Prompt Library</b>, and run the prompt below."],
      prompt="From /My Prompt Library, find my prompt for [the task you need now]. Show it to me with the [brackets] filled in for this case: [describe the case]. Then run it.",
      findings=[{"label": "The three prompts you added (names)", "hint": ""}, {"label": "Did Copilot find and reuse the right one?", "hint": "yes / no — what happened"}],
      expect="A Word file in your OneDrive with at least eight tested prompts — five from the template and three of your own — and one reused from Copilot with <kbd>/</kbd>.",
      stretch="In Word, ask Copilot: <i>“Group these prompts by app and add a one-line ‘when to use it’ for any row that is missing one.”</i> Check it didn't change the prompts themselves.",
      boss="Ask Copilot in Word: <i>“Which of these prompts are missing a Format or a Tone? Suggest one line to add to each.”</i> Accept only the suggestions you agree with."),
 dict(id="E2.7", app="Built-in agents", title="Use a built-in agent", minutes="10 min", block="Block 3 · Agents",
      scenario="Microsoft ships agents that are ready to use. <b>Analyst</b> turns raw data into findings and charts. <b>Prompt Coach</b> helps you structure prompts. Use both — and check Analyst's numbers against the answers you already trust from Day 1.",
      files=[{"label": "amfo-q3-custody-export.xlsx · Al-Murjan custody export (30 Sep)", "href": "amfo-q3-custody-export.xlsx",
              "note": "The same raw export you cleaned on Day 1. Save it to your <b>OneDrive</b>."}],
      steps=[f"Open the Copilot app ({COP}). In the left panel, select <b>Agents</b> → <b>Analyst</b>.",
             "Attach the Al-Murjan export (<b>+</b> → upload, or type <kbd>/</kbd> and pick it from OneDrive). Run prompt 1 below. Watch it show its working.",
             "Compare its answers with your Day 1 numbers. Write down any difference — and why it happened.",
             "Now open <b>All agents</b> → <b>Prompt Coach</b> (add it if you need to). Paste one prompt from your Word library and run prompt 2. Take one suggestion and save the better version in your library."],
      prompts=[{"label": "1 · Analyst", "text": "This is a custody export for a family office client. Remove duplicate holdings by Holding ID, fill any missing 30 Sep prices from the Price_List sheet, and convert USD to KWD at 0.3065. Then give me: total value at 30 Sep in KWD, the weight of each asset class against the Mandate sheet, and any single issuer above 10% of the portfolio (shares and bonds together). Show your working."},
               {"label": "2 · Prompt Coach", "text": "Here is a prompt I use at work. Tell me what is missing using Context, Task, Format and Tone, and give me one improved version: [paste a prompt from your library]"}],
      fallback="No <b>Agents</b> in your left panel? Your administrator may not have switched them on — that is normal. Run prompt 1 in Copilot Chat with the file attached instead, and compare in the same way.",
      findings=[{"label": "Analyst's total and equity weight", "hint": "KWD · %"}, {"label": "Any difference from your Day 1 answer — and why", "hint": ""}, {"label": "The Prompt Coach suggestion you kept", "hint": ""}],
      reveal="Day 1 answers: total <b>KWD 4,696,424</b> · Equity <b>61.0%</b> (above the 55% maximum) · <b>Al-Noor Bank 12.21%</b> (shares + sukuk, above 10%). If Analyst's total is about <b>KWD 5.79 million</b>, it kept the duplicates. If Al-Noor Bank shows below 10%, it counted the shares only.",
      expect="One agent answer checked against numbers you trust — and one prompt in your library made better.",
      stretch="Ask Analyst for a chart of allocation against the mandate range. Would you put it in a client deck as it is?",
      boss="Open <b>Researcher</b>. Ask for a one-page brief on what drove GCC bank shares in Q3 2026, with sources. Pick one claim and open its source. Does the source say what Researcher says?"),
 dict(id="E2.8", app="Agent Builder", title="Build the Request Triage Assistant", minutes="20 min", block="Block 3 · Agents",
      scenario="Every Sunday, Faisal's team reads forty client requests to find the client, the ask, the deadline and the risks. Build <b>Request Triage Assistant</b>: an agent that does the reading and flags what breaks KAMCO's client rules. Then test it six ways — each test should get a <b>different kind of answer</b>.",
      files=HV,
      briefs=[{"label": "Test material · the Al-Murjan thread", "text": THREAD}],
      steps=["Download the house view (above). In Copilot, select <b>New agent</b>. Agent Builder opens: a <b>chat</b> on the left, the <b>Configure</b> panel on the right.",
             "<b>Describe:</b> in the chat box on the left, write a description that reaches the build goal below. Watch the right side fill in: the name, the description and <b>Instructions</b>. Read the Instructions. Fix anything wrong by typing in the box.",
             "<b>Knowledge:</b> under <b>Knowledge</b>, add the house view. Turn <b>Web search</b> off, so it answers from your files and what you paste.",
             "<b>Suggested prompts:</b> add two. For example, Title <i>Triage a request</i> · Message <i>Triage this request: [paste the email]</i>",
             "<b>Test:</b> switch to <b>Preview</b>. Run the six tests below and note what it said. Switch back to <b>Configure</b> to make changes.",
             "<b>Fix:</b> pick the worst answer. Change one line in <b>Instructions</b> and test again. Then select <b>Create</b>. Keep it private — don't share it today."],
      fallback="No <b>New agent</b> in your Copilot? Your IT team may have switched Agent Builder off — that is normal. Do the same work in Copilot Chat: paste your description as the first message, upload the house view with <b>+</b>, then run the six tests. Same lesson: instructions + knowledge + testing.",
      promptSteps=[
          {"label": "Build · Describe the agent", "goal": "An agent that reads client requests for KAMCO wealth management staff. For any email or thread it gives: the client, each requested output and its format, the final deadline (always the newest message), who to copy — and flags anything that breaks section 4 of the house view. Answers in a table. Says so when something is unclear.",
           "prompt": "Create an agent called Request Triage Assistant. It helps KAMCO wealth management staff read client requests. For any email or thread I paste, give: 1) the client name; 2) each requested output and its format; 3) the final deadline - always use the newest message when instructions change; 4) who must be copied; 5) any request that breaks the client communication rules in section 4 of the house view, such as sharing another client's data or promising returns. Answer in a table. If something is unclear, say so - do not guess."},
          {"label": "Test 1 · A normal request", "goal": "Paste the Al-Murjan thread (above) and ask it to triage it.",
           "prompt": "Triage this request: [paste the Al-Murjan thread]",
           "findings": [{"label": "Deadline it gave", "hint": "is it the newest one?"}]},
          {"label": "Test 2 · Another client's data", "goal": "Does it flag Khalid's request for the Al-Rumaithiya report?",
           "findings": [{"label": "Did it flag it?", "hint": "yes / no — and how"}]},
          {"label": "Test 3 · A promise of returns", "goal": "Ask it to draft a line telling a client “you will earn at least 8% next year”.",
           "prompt": "Draft one line for the client: you will earn at least 8% next year with our recommended portfolio.",
           "findings": [{"label": "What it did", "hint": "refused, warned, or wrote it?"}]},
          {"label": "Test 4 · Not in the files", "goal": "Ask something the house view does not cover, e.g. our view on gold.",
           "prompt": "What is KAMCO's house view on gold for Q4?",
           "findings": [{"label": "Did it admit it does not know?", "hint": ""}]},
          {"label": "Test 5 · A vague request", "goal": "Paste a two-line email with no deadline and no client name.",
           "prompt": "Triage this request: Hi, can you send the numbers for the meeting? Thanks.",
           "findings": [{"label": "Did it ask, or guess?", "hint": ""}]},
          {"label": "Test 6 · Fix and retest", "goal": "Pick the worst answer. Change one line in Instructions. Run that test again.",
           "findings": [{"label": "The line you changed — and did it work?", "hint": ""}]}],
      reveal="<ul><li>Test 1: deadline <b>Tue 13 Oct, 3:00 pm</b> (not Wednesday); 5-slide deck + one-page memo; copy <b>Noura in Compliance</b>.</li><li>Test 2: it should flag the <b>Al-Rumaithiya report</b> — another client's data.</li><li>Test 3: it should refuse or warn — <b>never promise a return</b> (house view section 4).</li><li>Test 4: it should say the house view does not cover gold — not invent a view.</li><li>Test 5: it should list what is missing (client, deadline, which numbers) instead of guessing.</li></ul>",
      expect="An agent that finds the newest deadline, flags the two rule-breakers, admits what it doesn't know — and one instruction you fixed after testing.",
      stretch="Add a third suggested prompt: <i>“Draft a polite reply that declines the request that breaks our rules.”</i> Test it on the Al-Murjan thread.",
      boss="Write one test that would fool your agent. Then change the Instructions so it can't."),
 "__CAPSTONE__",
 dict(id="E2.10", app="Wrap up", title="MAP test, survey — and take it home", minutes="15:00 · 15:30", block="Close",
      scenario="Two short things close the program. At 15:00 you retake the MAP test — the same test as Sunday morning, so you can see how far you travelled. At 15:30, tell us how it landed while it's fresh. Then certificates.",
      launches=[{"link": "mapPost", "label": "1 · MAP test — post (15:00)", "note": "The same test as Sunday. 30 minutes. Answer honestly."},
                {"link": "survey", "label": "2 · Satisfaction survey (15:30)", "note": "What worked, what didn't, what you'd change. About 5 minutes."}],
      steps=["At 15:00, open the MAP test above and complete it.", "At 15:30, open the survey. Certificates follow by name.",
             "Before you leave: save your best prompts from the two days to <b>Your prompts</b> in Copilot."],
      expect="Both links done — and your best prompts saved where you'll find them next week."),
]

SITE = {"links": {"mapPost": "https://portal.joincoded.com/sv/kamco-copilot-map-test-post-day-2",
                  "survey": "https://portal.joincoded.com/sv/kamco-copilot-end-of-program-satisfaction-survey"}}

if __name__ == "__main__":
    import json
    from capstone_lab import capstone_task, patch_roles
    cap = json.load(open("out/capstone.json"))
    from agent_lab import agent_task
    TASKS = [capstone_task(cap) if t == "__CAPSTONE__" else (agent_task(t) if isinstance(t, dict) and t.get("id") == "E2.8" else t) for t in TASKS]
    build("out/site/coded-kamco-day-2-lab.html", back="coded-kamco-day-2.html", tasks=TASKS, day=2,
          chip="Day 2 · From Insight to Output", key="kamco_copilot_day2_tasks", site=SITE)
    fn = "out/site/coded-kamco-day-2-lab.html"
    html = patch_roles(open(fn, encoding="utf-8").read())
    open(fn, "w", encoding="utf-8").write(html)
    print("task lab day 2:", len(TASKS), "tasks")
