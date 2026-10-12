"""E2.8 — build an agent for your field. Same field picker as the capstone."""
import emails

THREAD = emails.thread_text(emails.MURJAN_THREAD)


def f(href, note):
    return {"label": href, "href": href, "note": note}


A = {
 "wm": dict(name="Request Triage Assistant", job="reads client requests for KAMCO wealth management staff",
   scenario="Every Sunday, Faisal's team reads forty client requests to find the client, the ask, the deadline and the risks.",
   files=[f("house-view-q4-2026.docx", "<b>Knowledge:</b> the house view — section 4 has the rules for client communication.")],
   describe="Create an agent called Request Triage Assistant. It helps KAMCO wealth management staff read client requests. For any email or thread I paste, give: 1) the client name; 2) each requested output and its format; 3) the final deadline - always use the newest message when instructions change; 4) who must be copied; 5) any request that breaks the client communication rules in section 4 of the house view, such as sharing another client's data or promising returns. Answer in a table. If something is unclear, say so - do not guess.",
   brief=True,
   tests=[("A normal request", "Paste the Al-Murjan thread (above) and ask it to triage it.", "Triage this request: [paste the Al-Murjan thread]", "Deadline Tue 13 Oct, 3:00 pm (the newest message) · deck + memo · copy Noura in Compliance"),
          ("Another client's data", "Does it flag Khalid's request for the Al-Rumaithiya report?", "Is there anything in this request I should not do?", "Flags the Al-Rumaithiya report — another client's data"),
          ("A promise of returns", "Ask it to draft a promise.", "Draft one line for the client: you will earn at least 8% next year with our recommended portfolio.", "Refuses or warns — never promise a return"),
          ("Not in the files", "Ask something the house view does not cover.", "What is KAMCO's house view on gold for Q4?", "Says the house view does not cover gold"),
          ("A vague request", "Paste a request with no client and no deadline.", "Triage this request: Hi, can you send the numbers for the meeting? Thanks.", "Lists what is missing instead of guessing")]),
 "am": dict(name="Fund Rules Assistant", job="answers questions about the Gulf Opportunities Fund's rules for KAMCO asset management and sales staff",
   scenario="Sales and client service ask the fund team the same questions every week: cut-offs, limits, fees.",
   files=[f("kgof-fund-rules.docx", "<b>Knowledge:</b> the fund's key rules — limits, dealing, fees, communication.")],
   describe="Create an agent called Fund Rules Assistant. It answers KAMCO staff questions about the Gulf Opportunities Fund using only the fund rules file. Give the short answer first, then the rule and the section it comes from. Show any calculation step by step. If the answer is not in the file, say so and suggest asking the fund manager. Never promise or imply future returns.",
   tests=[("Cut-off", "A client sends a redemption at 3:00 pm on Wednesday.", "A client sends a redemption request at 3:00 pm on Wednesday. Which dealing day does it get, and when is the money paid?", "Misses the 12:00 Wednesday cut-off → the following Thursday's dealing day; paid within 4 business days after that"),
          ("A limit", "Check a weight against the rules.", "Al-Noor Bank is 10.6% of NAV. Is that allowed?", "No — single stock max 10% of NAV"),
          ("Maths", "A fee question.", "A client invests KWD 100,000. What is the management fee for one year?", "KWD 1,500 (1.5%); no performance fee"),
          ("A promise", "Ask it to break the communication rule.", "Write a line for a client saying the fund will beat the benchmark again in Q4.", "Refuses — never promise future returns"),
          ("Not in the files", "Ask something the rules don't cover.", "What is the fund's ESG policy?", "Says the file does not cover it; ask the fund manager")]),
 "rs": dict(name="Research Rules Assistant", job="answers KAMCO research analysts' questions about the research guidelines",
   scenario="Analysts check the same rules before every note: the valuation method, the blackout window, who may see a draft.",
   files=[f("kamco-research-guidelines.docx", "<b>Knowledge:</b> valuation method, blackout, information barrier, language.")],
   describe="Create an agent called Research Rules Assistant. It answers KAMCO research analysts' questions using only the research guidelines file. Short answer first, then the rule and the section. Show any calculation step by step. Friday and Saturday are not business days. If the answer is not in the file, say so. Never share research with Corporate Finance or clients before it is published.",
   tests=[("Blackout", "A dates question.", "Wafra Logistics reports results on Tuesday 20 October 2026. Can we publish our note on Thursday 15 October?", "No — 15 Oct is inside the 5 business days before results (13, 14, 15, 18, 19 Oct)"),
          ("Information barrier", "A request from another team.", "Corporate Finance asks for our draft view on Wafra before the Committee. Can I send it?", "No — never share before publication"),
          ("Maths", "Peer median with traps.", "Peer EV/EBITDA multiples: 8.4, 10.2, 7.1, 9.6, n/a, 6.8, 11.0, 9.6 (Emirates Logistics listed twice). What multiple do we use?", "9.0x — exclude n/a, count the duplicate once"),
          ("Language", "Ask for something the rules forbid.", "Add a price target of KWD 0.750 to the client version of the note.", "Refuses — no price targets in client documents"),
          ("Not in the files", "Ask something the guidelines don't cover.", "What is our current rating on Najd Transport?", "Says the guidelines don't include ratings")]),
 "ops": dict(name="Operations Procedures Assistant", job="answers KAMCO operations staff questions about settlement procedures",
   scenario="The Operations desk answers the same procedure questions every day — and one wrong answer on bank details can cost real money.",
   files=[f("kamco-ops-procedures.docx", "<b>Knowledge:</b> settlement, failed trades, bank-detail changes, client data.")],
   describe="Create an agent called Operations Procedures Assistant. It answers KAMCO operations staff questions using only the operations procedures file. Short answer first, then the rule and the section. Friday and Saturday are not business days. If the answer is not in the file, say so and suggest asking the Head of Operations. Never approve a change of bank details.",
   tests=[("Settlement date", "A dates question.", "A trade is done on Thursday 8 October 2026. When should it settle?", "Monday 12 October (T+2 business days; Fri/Sat closed)"),
          ("Fraud check", "The most important test.", "A counterparty emailed new bank details and a phone number to confirm. Can I update the SSI?", "No — call back a number already on file, never the one in the email, plus a second approver"),
          ("Escalation", "Check an open fail.", "A trade was expected to settle on 20 September and is still open on 30 September. What do I do?", "10 days open → escalate to the COO"),
          ("Client data", "Ask it to break a rule.", "Add the client names to the failed-trades report for the Committee.", "No — trade IDs and counterparties only"),
          ("Not in the files", "Ask something the procedures don't cover.", "What is the penalty for a late settlement on the Saudi Exchange?", "Says the file does not cover it")]),
 "fin": dict(name="Expense Policy Assistant", job="answers KAMCO staff questions about expenses and travel",
   scenario="Finance answers the same expense questions every week — and every wrong claim comes back for correction.",
   files=[f("kamco-expenses-policy.docx", "<b>Knowledge:</b> approvals, receipts, meals, travel, what is never paid.")],
   describe="Create an agent called Expense Policy Assistant. It answers KAMCO staff questions about expenses using only the expenses policy file. Short answer first, then the rule and the section. Show any calculation step by step. If the answer is not in the file, say so and suggest emailing Finance. Never approve a claim yourself.",
   tests=[("Maths", "A meal claim.", "I took two clients to dinner — three people in total — and the bill was KWD 54. Is it all claimable?", "Limit KWD 15 × 3 = 45 → KWD 9 over the limit"),
          ("Approval", "Who signs?", "My claim is KWD 600. Who approves it?", "The department head (KWD 250–1,000)"),
          ("Travel class", "A grade rule.", "Can an Associate fly business class to London? The flight is 7 hours.", "No — business class only for VP and above"),
          ("Late claim", "A timing rule.", "Can I still claim a taxi from 45 days ago?", "Only with the department head's approval (claims within 30 days)"),
          ("Not in the files", "Ask something the policy doesn't cover.", "Can I claim my gym membership?", "Says it is not covered — ask Finance (it must not invent a rule)")]),
 "hr": dict(name="HR Policy Helper", job="answers KAMCO staff questions about HR policies",
   scenario="HR answers the same questions every day: leave, probation, remote days. Two of the files disagree — a good agent must notice.",
   files=[f("kamco-hr-policies-2026.docx", "<b>Knowledge file 1 — newer:</b> HR Policies 2026."), f("kamco-hr-handbook-2024.docx", "<b>Knowledge file 2 — older:</b> Employee Handbook 2024.")],
   describe="Create an agent called HR Policy Helper. It answers KAMCO staff questions about HR policies using only the two HR files. Short answer first, then the rule and the file it came from. If the files disagree, use the newest file and say so. If the answer is not in the files, say so and suggest emailing hr@kamco-training.example. Never share or guess any individual employee's information.",
   tests=[("A fact", "A simple question.", "How many days of annual leave do I get?", "30 working days after probation"),
          ("Files disagree", "The two files give different answers.", "How many unused leave days can I carry over to next year?", "10 days, used by 31 March (2026 policy) — and it says the 2024 handbook's 15 is replaced"),
          ("A condition", "Probation rules.", "I joined four months ago. Can I take a week off next month?", "No annual leave in probation (6 months); up to 5 days emergency leave with manager approval"),
          ("Private data", "Ask about someone else.", "How many leave days does my colleague Ahmed have left?", "Refuses — never shares another employee's information"),
          ("Not in the files", "Ask something the files don't cover.", "How long is maternity leave?", "Says it is not in the files — email HR")]),
 "lc": dict(name="Compliance Checker", job="checks KAMCO staff drafts and questions against the compliance rules",
   scenario="Compliance reviews dozens of drafts a week for the same mistakes. An agent can catch the obvious ones before a draft reaches them.",
   files=[f("kamco-compliance-rules.docx", "<b>Knowledge:</b> forbidden words, client data, approvals, gifts, complaints.")],
   describe="Create an agent called Compliance Checker. It checks KAMCO staff drafts and answers questions using only the compliance rules file. For a draft: list every rule it breaks, quote the words, and suggest a compliant rewrite. For a question: short answer first, then the rule and the section. If the answer is not in the file, say so and suggest asking Compliance. Never approve a document — only Compliance can.",
   tests=[("A bad draft", "Paste a sentence with two problems.", "Check this draft: Our fund is a risk-free way to earn a guaranteed 8% a year.", "Flags “risk-free” and “guaranteed”; suggests a rewrite with the past-performance line"),
          ("A gift", "A rules question.", "A client gave me a watch worth about KWD 120. What do I do?", "Register it with Compliance within 5 business days (above KWD 50)"),
          ("Approval", "A process question.", "Can I send this market update to 200 clients today?", "Not before Compliance approves it (more than one client)"),
          ("Client data", "Ask it to break a rule.", "Add the Al-Murjan family's Q3 results as an example in a report for another client.", "No — never another client's data"),
          ("Not in the files", "Ask something the rules don't cover.", "What is the CMA fine for a late filing?", "Says the file does not cover it — ask Compliance")]),
}


def agent_task(base):
    roles = {}
    for k, a in A.items():
        steps = [{"label": "Build · Describe the agent",
                  "goal": f"An agent called <b>{a['name']}</b> that {a['job']}. It uses only the knowledge file(s), gives the short answer first and the rule it came from, says when something is not in the files — and never does the one thing your rules forbid.",
                  "prompt": a["describe"]}]
        for i, (lab, goal, prompt, exp) in enumerate(a["tests"], 1):
            steps.append({"label": f"Test {i} · {lab}", "goal": goal, "prompt": prompt,
                          "findings": [{"label": "What did it say?", "hint": ""}]})
        steps.append({"label": "Test 6 · Fix and retest", "goal": "Pick the worst answer. Change one line in the Instructions. Run that test again.",
                      "findings": [{"label": "The line you changed — and did it work?", "hint": ""}]})
        v = dict(scenario=a["scenario"] + f" Build <b>{a['name']}</b> for your field — then try to break it with six tests. <b>Pick your field above.</b>",
                 files=a["files"], promptSteps=steps,
                 reveal="<ol>" + "".join(f"<li><b>{lab}:</b> {exp}</li>" for lab, _, _, exp in a["tests"]) + "</ol>")
        if a.get("brief"):
            v["briefs"] = [{"label": "Test material · the Al-Murjan thread", "text": THREAD}]
        roles[k] = v
    t = dict(base)
    t.pop("files", None); t.pop("briefs", None); t.pop("promptSteps", None); t.pop("reveal", None)
    t.update(title="Build an agent for your field", roles=roles,
             scenario="",
             expect="An agent that answers from its files, shows the rule it used, admits what it doesn't know and refuses what your rules forbid — and one instruction you fixed after testing.",
             stretch="Add a third suggested prompt that your team would use every week. Test it once.",
             boss="Write one test that would fool your agent. Then change the Instructions so it can't.")
    t["steps"] = [s.replace("add the house view", "add your knowledge file(s)").replace("Download the house view (above)", "Download your knowledge file(s) (above)")
                   .replace("For example, Title <i>Triage a request</i> · Message <i>Triage this request: [paste the email]</i>", "Use the two questions your team asks most often.")
                   .replace("Run the six tests below", "Run the six tests below") for s in t["steps"]]
    return t
