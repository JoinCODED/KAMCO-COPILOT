"""Capstone data — four KAMCO fields. Each field: an email thread (instructions change), a messy Excel workbook
with a Policy sheet, and computed reference answers for the facilitator. All data is fictional."""
import json, os, random, datetime as dt, statistics
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from email.message import EmailMessage

OUT = "out/files"
A = json.load(open("out/answers.json"))
HDR = Font(bold=True, color="FFFFFF"); FILL = PatternFill("solid", fgColor="1F3A68")
D = dt.date


def title_rows(ws, title, note):
    ws.append([title]); ws["A1"].font = Font(bold=True, size=13)
    ws.append([note]); ws.append([])


def header(ws, cols):
    ws.append(cols)
    r = ws.max_row
    for c in ws[r]:
        c.font = HDR; c.fill = FILL
    for i, _ in enumerate(cols):
        ws.column_dimensions[chr(65 + i) if i < 26 else "A"].width = 18


def thread(msgs):
    """msgs newest first: (from, sent, to, body)"""
    out = []
    for i, (f, s, t, b) in enumerate(msgs):
        out.append(f"From: {f}\nSent: {s}\nTo: {t}\n\n{b}")
    return ("\n\n" + "-" * 40 + "\n\n").join(out)


def eml(fn, subject, frm, body, attach=None):
    m = EmailMessage(); m["Subject"] = subject; m["From"] = frm; m["To"] = "you@kamco-training.example"
    m.set_content(body)
    if attach:
        data = open(os.path.join(OUT, attach), "rb").read()
        m.add_attachment(data, maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=attach)
    open(os.path.join(OUT, fn), "wb").write(bytes(m))


KEY = {}

# =====================================================================  1 · WEALTH MANAGEMENT
B = A["bayan"]
WM_SUBJ = "RE: Al-Bayan Holding - Q3 review for the Investment Committee"
WM_THREAD = thread([
 ("Huda Al-Enezi (Investment Committee Secretary)", "Mon 12 Oct 2026, 13:25", "You",
  "Hi,\n\nUpdate: the Committee has moved Al-Bayan to the top of tomorrow's agenda, so I need everything from you today by 2:50 pm - not Wednesday.\n\n"
  "Please send TWO files:\n1) A one-page executive brief in Word for the Committee (internal - no client disclaimer).\n"
  "2) A 6-slide PowerPoint deck that Yousef can use with the client on Thursday (client-facing - add the standard disclaimer from the house view).\n\n"
  "Include at least one chart of allocation against the mandate ranges.\n\nThanks,\nHuda"),
 ("Fahad Al-Bayan (CFO, Al-Bayan Holding)", "Sun 11 Oct 2026, 18:10", "Yousef Al-Kandari",
  "Dear Yousef,\n\nAhead of our review: the family is worried about property. How much of the portfolio is now in real estate, and is any single name too big?\n\n"
  "Also, could you share how the Al-Murjan family portfolio did this quarter? We would like to compare.\n\nRegards,\nFahad"),
 ("Huda Al-Enezi (Investment Committee Secretary)", "Thu 8 Oct 2026, 09:40", "You",
  "Hi,\n\nPlease prepare the Q3 review of Al-Bayan Holding for the Investment Committee on Wednesday 14 Oct. Use the 30 Sep custody export attached.\n\n"
  "Cover: value at 30 Sep and Q3 change (KWD and %), allocation against the mandate, the 10% single-issuer check, top 3 and bottom 3 contributors, and your recommendation.\n\nThanks,\nHuda")])
KEY["wm"] = dict(file=B["file"], deadline="Today, 2:50 pm (moved from Wednesday)", deliverables="1-page Word brief (internal, no disclaimer) + 6-slide client deck (with disclaimer) + at least one allocation chart",
                 decline="Fahad's request for the Al-Murjan portfolio results — another client's data",
                 numbers=[("Raw rows / duplicates / holdings", f"{B['raw_rows']} / {B['duplicates']} / {B['holdings']}"),
                          ("Missing 30 Sep prices", ", ".join(B["missing_tickers"])),
                          ("Total value 30 Sep", f"KWD {B['total_sep']:,}"), ("Wrong total if duplicates kept", f"KWD {B['wrong_if_dups_kept']:,}"),
                          ("Q3 change", f"KWD {B['q3_change']:,} ({B['q3_return_pct']}%)"),
                          ("Allocation", " · ".join(f"{k} {v}%" for k, v in B["alloc_pct"].items())),
                          ("Mandate breach", "Real Estate 19.4% — above the 15% maximum"),
                          ("Issuer breach", "Gulf Horizon REIT 11.11% — above 10%"),
                          ("Top 3", ", ".join(f"{n} (+{v:,})" for n, v in B["top3"])),
                          ("Bottom 3", ", ".join(f"{n} ({v:,})" for n, v in B["bottom3"]))],
                 recommend="Trim real estate back inside 5–15% — starting with Gulf Horizon REIT to get it below 10% — and move the proceeds towards fixed income, in line with the house view (Real Estate: Cautious; Fixed Income: Positive).")

# =====================================================================  2 · ASSET MANAGEMENT
random.seed(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"]
fund = [1.8, -0.6, 2.4, 1.1, -1.9, 0.7, 2.9, -0.8, 1.6]
bench = [1.5, -0.2, 1.9, 1.3, -1.4, 0.9, 2.1, -0.5, 1.2]
holds = [("Al-Noor Bank", "Banks", 9.4, 10.6, 11.2), ("Gulf Trade Bank", "Banks", 8.1, 7.9, -2.7), ("Kuwait Finance Partners", "Banks", 7.6, 8.3, 6.4),
         ("Doha Commercial Bank", "Banks", 6.2, 6.0, 1.8), ("Riyadh Capital Bank", "Banks", 5.0, 5.4, 4.9), ("Bayan Telecom", "Telecom", 7.2, 7.0, 3.5),
         ("Gulf Mobile Co.", "Telecom", 4.1, 3.8, -4.2), ("Jaber Cement", "Materials", 4.6, 4.9, 6.8), ("Arabian Petrochem", "Materials", 5.5, 5.1, -3.9),
         ("Sadaf Logistics", "Industrials", 4.8, 4.2, -10.1), ("Najd Industrial", "Industrials", 5.2, 4.9, -6.3), ("Failaka Foods", "Consumer", 4.4, 4.6, 4.8),
         ("Marina Retail Group", "Consumer", 3.9, 4.1, 5.6), ("Gulf Horizon REIT", "Real Estate", 4.0, 3.6, -8.9), ("Salmiya Properties", "Real Estate", 3.3, 3.2, -1.5),
         ("Emirates Power Co.", "Utilities", 3.7, 3.9, 5.2), ("Qurain Healthcare", "Healthcare", 3.0, 3.2, 7.4)]
cash_w = 100 - sum(h[3] for h in holds)
holds.append(("Cash & deposits", "Cash", round(100 - sum(h[2] for h in holds), 1), round(cash_w, 1), 0.0))
flows = [(m, ch, s, r) for m, s1, r1, s2, r2 in [("Jan", 1250, 420, 610, 380), ("Feb", 980, 1310, 540, 410), ("Mar", 1420, 600, 720, 350), ("Apr", 860, 940, 480, 520),
                                                 ("May", 640, 2150, 390, 610), ("Jun", 1100, 700, 560, 300), ("Jul", 1890, 520, 830, 290), ("Aug", 760, 1180, 450, 470), ("Sep", 1340, 610, 690, 330)]
         for ch, s, r in [("Institutional", s1, r1), ("Retail", s2, r2)]]
wb = Workbook(); ws = wb.active; ws.title = "Monthly_Returns"
title_rows(ws, "KAMCO Gulf Opportunities Fund (training) - monthly returns 2026", "Source: fund admin export. Returns in % per month. Training sample - fictional.")
header(ws, ["Month", "Fund return %", "Benchmark return %"])
for i, m in enumerate(months):
    ws.append([m + "-2026", fund[i] if i != 4 else str(fund[i]), bench[i]])  # May fund return stored as text
ws2 = wb.create_sheet("Holdings_30Sep")
title_rows(ws2, "Holdings - weights in % of NAV", "Q3 return = total return of the holding from 30 Jun to 30 Sep, in %.")
header(ws2, ["Holding", "Sector", "Weight 30-Jun %", "Weight 30-Sep %", "Q3 return %"])
for h in holds:
    ws2.append(list(h))
ws2.append(["Al-Noor Bank", "Banks", 9.4, 10.6, 11.2])  # duplicate row
ws3 = wb.create_sheet("Flows")
title_rows(ws3, "Subscriptions and redemptions by month (KWD '000)", "Net flow = subscriptions - redemptions.")
header(ws3, ["Month", "Channel", "Subscriptions", "Redemptions"])
for i, f in enumerate(flows):
    ws3.append([f[0], f[1] if i != 5 else "institutional ", f[2], f[3] if i != 9 else f"{f[3]:,}"])
ws4 = wb.create_sheet("Policy")
title_rows(ws4, "Fund rules (prospectus, training version)", "")
for r in [["Rule", "Limit"], ["Single stock", "max 10% of NAV"], ["Single sector", "max 35% of NAV"], ["Cash", "2% to 10% of NAV"],
          ["NAV at 30 Sep 2026", "KWD 48,600,000"], ["Benchmark", "GCC Composite Index (training)"],
          ["Reporting", "Returns to one decimal place. Never promise or imply future returns."]]:
    ws4.append(r)
wb.save(os.path.join(OUT, "kgof-q3-fund-pack.xlsx"))


def comp(rs):
    v = 1.0
    for r in rs:
        v *= 1 + r / 100
    return round((v - 1) * 100, 2)


sect = {}
for h in holds:
    sect[h[1]] = sect.get(h[1], 0) + h[3]
contrib = sorted(((h[0], round(h[2] * h[4] / 100, 2)) for h in holds if h[1] != "Cash"), key=lambda x: -x[1])
net = {}
for m, ch, s, r in flows:
    net[m] = net.get(m, 0) + s - r
ytd_net = sum(net.values()); q3_net = net["Jul"] + net["Aug"] + net["Sep"]
best = max(range(9), key=lambda i: fund[i] - bench[i]); worst = min(range(9), key=lambda i: fund[i] - bench[i])
AM_SUBJ = "RE: Gulf Opportunities Fund - Q3 board pack"
AM_THREAD = thread([
 ("Dalal Al-Sabah (Chief Investment Officer)", "Mon 12 Oct 2026, 13:20", "You",
  "Hi,\n\nThe fund board call has been brought forward to tomorrow at 9:00, so I need your files today by 2:50 pm.\n\n"
  "Two files please:\n1) A one-page executive brief in Word for me (internal).\n2) A 6-slide PowerPoint for the board, with a chart of cumulative fund vs benchmark return since January.\n\n"
  "Lead with whether we are inside the fund rules. Use one decimal place for every return.\n\nThanks,\nDalal"),
 ("Bader Al-Mutawa (Distribution)", "Sun 11 Oct 2026, 16:05", "Dalal Al-Sabah",
  "Dalal,\n\nTwo big institutional clients are asking about the fund. Can the board deck include a line saying we expect to beat the benchmark again in Q4? It would really help sales.\n\nBader"),
 ("Dalal Al-Sabah (Chief Investment Officer)", "Wed 7 Oct 2026, 11:15", "You",
  "Hi,\n\nPlease prepare the Q3 review of the Gulf Opportunities Fund for the board on Thursday 15 Oct, using the attached fund pack.\n\n"
  "Cover: fund vs benchmark - year to date and Q3; best and worst month against the benchmark; sector and single-stock weights against the fund rules; top 3 and bottom 3 contributors in Q3; and net flows.\n\nThanks,\nDalal")])
KEY["am"] = dict(file="kgof-q3-fund-pack.xlsx", deadline="Today, 2:50 pm (moved from Thursday)", deliverables="1-page Word brief (internal) + 6-slide board deck with a cumulative return chart",
                 decline="Bader's line that we 'expect to beat the benchmark in Q4' — a promise about future returns",
                 numbers=[("Data issues", "May fund return stored as text · Al-Noor Bank listed twice in holdings · one channel label with a trailing space · one redemption stored as text"),
                          ("YTD return Jan–Sep (compounded)", f"Fund {comp(fund):.2f}% vs benchmark {comp(bench):.2f}% → excess {comp(fund)-comp(bench):+.2f} pts (report as {comp(fund):.1f}% vs {comp(bench):.1f}%)"),
                          ("Q3 return (Jul–Sep)", f"Fund {comp(fund[6:]):.2f}% vs benchmark {comp(bench[6:]):.2f}%"),
                          ("Best month vs benchmark", f"{months[best]} ({fund[best]-bench[best]:+.1f} pts)"), ("Worst month vs benchmark", f"{months[worst]} ({fund[worst]-bench[worst]:+.1f} pts)"),
                          ("Sector weights 30 Sep", " · ".join(f"{k} {v:.1f}%" for k, v in sorted(sect.items(), key=lambda x: -x[1]))),
                          ("Sector breach", f"Banks {sect['Banks']:.1f}% — above the 35% limit"),
                          ("Single-stock breach", "Al-Noor Bank 10.6% — above the 10% limit"),
                          ("Cash", f"{cash_w:.1f}% — inside 2–10%"),
                          ("Top 3 contributors (pts, weight 30 Jun × Q3 return)", ", ".join(f"{n} (+{v:.2f})" for n, v in contrib[:3])),
                          ("Bottom 3 contributors", ", ".join(f"{n} ({v:.2f})" for n, v in contrib[-3:][::-1])),
                          ("Net flows (KWD '000)", f"YTD {ytd_net:+,} · Q3 {q3_net:+,} · worst month May {net['May']:+,}")],
                 recommend="Bring Banks back below 35% and Al-Noor Bank below 10% at the next rebalance; report the outperformance without any forward-looking promise.")

# =====================================================================  3 · OPERATIONS
random.seed(7)
cps = [("Gulf Brokerage Co.", ["Gulf Brokerage Co.", "GULF BROKERAGE CO", "Gulf Brokerage"]), ("Al-Watani Securities", ["Al-Watani Securities"]),
       ("Riyadh Capital Markets", ["Riyadh Capital Markets", "Riyadh Capital Mkts"]), ("Emirates Trading House", ["Emirates Trading House"]),
       ("Atlantic Prime Brokers", ["Atlantic Prime Brokers"]), ("Kuwait Clearing Partners", ["Kuwait Clearing Partners"])]
mk = {"Gulf Brokerage Co.": "Boursa Kuwait", "Al-Watani Securities": "Boursa Kuwait", "Kuwait Clearing Partners": "Boursa Kuwait",
      "Riyadh Capital Markets": "Saudi Exchange", "Emirates Trading House": "ADX", "Atlantic Prime Brokers": "US"}
lateplan = {"Riyadh Capital Markets": [1, 3, 2, 6], "Atlantic Prime Brokers": [1, 2, 4], "Gulf Brokerage Co.": [1, 1], "Emirates Trading House": [2], "Al-Watani Securities": [], "Kuwait Clearing Partners": []}
start = D(2026, 7, 1)
trades = []
n = 0
day = start
while day <= D(2026, 9, 28):
    if day.weekday() in (4, 5):  # Fri, Sat closed
        day += dt.timedelta(days=1); continue
    for _ in range(random.choice([1, 2, 2])):
        n += 1
        cp = cps[n % 6][0]
        trades.append(dict(id=f"TRD-{26000 + n}", td=day, cp=cp, side=random.choice(["Buy", "Sell"]), val=random.randrange(40, 900) * 1000))
    day += dt.timedelta(days=1)


def addbd(d, k):
    while k > 0:
        d += dt.timedelta(days=1)
        if d.weekday() not in (4, 5):
            k -= 1
    return d


for t in trades:
    t["exp"] = addbd(t["td"], 2); t["act"] = t["exp"]; t["status"] = "Settled"
# assign lates deterministically
idx = {c: [t for t in trades if t["cp"] == c] for c, _ in cps}
for c, lates in lateplan.items():
    for k, days in enumerate(lates):
        t = idx[c][1 + k * 3]
        t["act"] = t["exp"] + dt.timedelta(days=days); t["status"] = "Settled late"
open_fails = [idx["Riyadh Capital Markets"][-6], idx["Atlantic Prime Brokers"][-3], idx["Gulf Brokerage Co."][-9]]
for t in open_fails:
    t["act"] = None; t["status"] = "Failed - open"
asof = D(2026, 9, 30)
wb = Workbook(); ws = wb.active; ws.title = "Trades_Q3"
title_rows(ws, "Settlement blotter export - Q3 2026 (1 Jul - 30 Sep)", "Source: back-office system. Values in KWD. Expected settlement = T+2 business days (Fri/Sat closed).")
header(ws, ["Trade ID", "Trade date", "Counterparty", "Market", "Side", "Value KWD", "Expected settle", "Actual settle", "Status"])
rows = []
for i, t in enumerate(trades):
    variants = dict(cps)[t["cp"]]
    name = variants[i % len(variants)]
    act = t["act"].isoformat() if (t["act"] and i % 17 == 5) else t["act"]  # some dates as text
    rows.append([t["id"], t["td"], name, mk[t["cp"]], t["side"], t["val"], t["exp"], act, t["status"]])
for r in rows:
    ws.append(r)
for r in [rows[10], rows[33], rows[57]]:
    ws.append(list(r))  # duplicates
ws2 = wb.create_sheet("Policy")
title_rows(ws2, "Settlement policy (training version)", "")
for r in [["Rule", "Detail"], ["On-time target", "98% of trades settle on the expected date"], ["Late", "Settled after the expected date (calendar days late = actual - expected)"],
          ["Escalate", "Any trade still open more than 5 calendar days after the expected date, as at 30 Sep 2026"],
          ["Counterparty review", "Any counterparty with 3 or more late or failed trades in a quarter"], ["Client names", "Never include client names in reports outside Operations"]]:
    ws2.append(r)
wb.save(os.path.join(OUT, "ops-q3-settlement-blotter.xlsx"))
tot = len(trades); ontime = sum(1 for t in trades if t["status"] == "Settled")
late = [t for t in trades if t["status"] == "Settled late"]
bad_by = {}
for t in trades:
    if t["status"] != "Settled":
        bad_by[t["cp"]] = bad_by.get(t["cp"], 0) + 1
esc = [(t["id"], t["cp"], (asof - t["exp"]).days, t["val"]) for t in open_fails if (asof - t["exp"]).days > 5]
by_month = {}
for t in trades:
    m = t["td"].strftime("%b"); a = by_month.setdefault(m, [0, 0]); a[0] += 1; a[1] += t["status"] == "Settled"
OPS_SUBJ = "RE: Q3 settlement review - Operations Committee"
OPS_THREAD = thread([
 ("Mishari Al-Ghanim (Chief Operating Officer)", "Mon 12 Oct 2026, 13:15", "You",
  "Hi,\n\nThe Operations Committee is now tomorrow at 8:30, so please send your files today by 2:50 pm.\n\n"
  "Two files:\n1) A one-page executive brief in Word for me.\n2) A 6-slide PowerPoint for the Committee, with a chart of late and failed trades by counterparty and the on-time rate by month.\n\n"
  "Lead with whether we met the 98% target, and list every trade I need to escalate.\n\nThanks,\nMishari"),
 ("Noura Al-Rashidi (Compliance)", "Sun 11 Oct 2026, 10:30", "Mishari Al-Ghanim",
  "Mishari,\n\nReminder for anything that goes to the Committee: no client names - trade IDs and counterparties only. Also, Riyadh Capital Markets asked for a copy of our internal counterparty scores; please do not share them outside KAMCO.\n\nNoura"),
 ("Mishari Al-Ghanim (Chief Operating Officer)", "Tue 6 Oct 2026, 14:00", "You",
  "Hi,\n\nPlease review Q3 settlement performance for the Operations Committee on Wednesday 14 Oct. The blotter export is attached.\n\n"
  "Cover: the on-time settlement rate against our 98% target, late and failed trades by counterparty, the average delay, the value of trades that settled late, and the open fails we must escalate.\n\nThanks,\nMishari")])
KEY["ops"] = dict(file="ops-q3-settlement-blotter.xlsx", deadline="Today, 2:50 pm (moved from Wednesday)", deliverables="1-page Word brief + 6-slide Committee deck with a counterparty chart and a monthly on-time chart",
                  decline="Sharing internal counterparty scores with Riyadh Capital Markets — and no client names in the Committee pack",
                  numbers=[("Data issues", "3 duplicate trade rows · counterparty name variants (Gulf Brokerage ×3 spellings, Riyadh Capital ×2) · some settle dates stored as text"),
                           ("Unique trades", f"{tot} (raw rows {tot + 3})"),
                           ("On time", f"{ontime} of {tot} = {ontime / tot * 100:.1f}% — below the 98% target"),
                           ("Settled late", f"{len(late)} trades · KWD {sum(t['val'] for t in late):,} · average {statistics.mean((t['act'] - t['exp']).days for t in late):.1f} days late"),
                           ("Open fails", ", ".join(f"{t['id']} ({t['cp']}, {(asof - t['exp']).days} days)" for t in open_fails)),
                           ("Escalate (open > 5 days)", ", ".join(f"{e[0]} · {e[1]} · {e[2]} days · KWD {e[3]:,}" for e in esc) or "none"),
                           ("Late or failed by counterparty", " · ".join(f"{k} {v}" for k, v in sorted(bad_by.items(), key=lambda x: -x[1]))),
                           ("Counterparty review (3+)", ", ".join(k for k, v in bad_by.items() if v >= 3)),
                           ("On-time by month", " · ".join(f"{m} {a[1]}/{a[0]} = {a[1] / a[0] * 100:.1f}%" for m, a in by_month.items()))],
                  recommend="Escalate the open fails over 5 days today; put Riyadh Capital Markets and Atlantic Prime Brokers on counterparty review; target the root cause (SSI and pre-matching) before Q4.")

# =====================================================================  4 · INVESTMENT RESEARCH
fin = {"Revenue": [41200, 46800, 52900, 28100], "EBITDA": [8650, 10060, 11900, 6180], "Net income": [4120, 5010, 6050, 3200],
       "Total debt": [22000, 24500, 23800, 23100], "Cash": [5400, 6100, 7300, 6900]}
shares = 180.0  # million
peers = [("Gulf Freight Holding", 8.4, 13.1, 9.5, 2.1), ("Arabian Ports Co.", 10.2, 16.4, 12.0, 1.4), ("Najd Transport", 7.1, 11.2, 4.8, 2.9),
         ("Emirates Logistics Group", 9.6, 15.0, 11.3, 1.8), ("Qatar Supply Chain", "n/a", 18.2, 14.6, 0.9), ("Oman Shipping & Storage", 6.8, 10.5, 3.9, 3.2),
         ("Saudi Cold Chain", 11.0, 19.8, 16.2, 1.1)]
prices = [0.512, 0.524, 0.531, 0.518, 0.540, 0.556, 0.549, 0.571, 0.588, 0.579, 0.601, 0.612, 0.598, 0.617, 0.633, 0.626, 0.641, 0.652]
pm = [D(2025, 4 + i, 1) if 4 + i <= 12 else D(2026, i - 8, 1) for i in range(18)]
wb = Workbook(); ws = wb.active; ws.title = "Financials"
title_rows(ws, "Wafra Logistics Co. - financial summary (KWD '000)", "FY = year to 31 Dec. H1 2026 = six months to 30 Jun (not annualised). Training sample - fictional.")
header(ws, ["Line item", "FY2023", "FY2024", "FY2025", "H1 2026"])
for k, v in fin.items():
    ws.append([k] + [x if not (k == "EBITDA" and j == 1) else f"{x:,}" for j, x in enumerate(v)])
ws.append(["Shares outstanding (million)", shares, shares, shares, shares])
ws2 = wb.create_sheet("Peers")
title_rows(ws2, "Listed GCC logistics peers - consensus multiples", "EV/EBITDA and P/E on FY2025. Revenue growth = FY2025 vs FY2024, %. Net debt/EBITDA = FY2025.")
header(ws2, ["Peer", "EV/EBITDA (x)", "P/E (x)", "Revenue growth %", "Net debt/EBITDA (x)"])
for p in peers:
    ws2.append(list(p))
ws2.append(list(peers[3]))  # duplicate
ws3 = wb.create_sheet("Share_Price")
title_rows(ws3, "Wafra Logistics - month-end share price (KWD)", "Boursa Kuwait close on the last trading day of each month.")
header(ws3, ["Month end", "Price KWD"])
for d_, p in zip(pm, prices):
    ws3.append([d_.strftime("%b-%Y"), p])
ws4 = wb.create_sheet("Policy")
title_rows(ws4, "Research valuation guidelines (training version)", "")
for r in [["Step", "Rule"], ["Valuation", "EV = peer median EV/EBITDA × FY2025 EBITDA. Exclude peers without a number. Count each peer once."],
          ["Equity value", "EV − net debt at FY2025 (total debt − cash)"], ["Per share", "Equity value ÷ shares outstanding"],
          ["Upside", "Value per share ÷ price at 30 Sep 2026 − 1"],
          ["View", "Upside above +15% = Attractive · −10% to +15% = Neutral · below −10% = Unattractive"],
          ["Language", "No price targets or promises in client documents. Internal committee use only."]]:
    ws4.append(r)
wb.save(os.path.join(OUT, "wafra-logistics-research-pack.xlsx"))
ev_x = statistics.median([p[1] for p in peers if isinstance(p[1], (int, float))])
ev = ev_x * fin["EBITDA"][2]; nd = fin["Total debt"][2] - fin["Cash"][2]; eq = ev - nd
vps = eq / (shares * 1000)  # KWD '000 / million shares = KWD per share ÷ 1000
vps = eq * 1000 / (shares * 1_000_000)
up = vps / prices[-1] - 1
view = "Attractive" if up > 0.15 else ("Neutral" if up >= -0.10 else "Unattractive")
cagr = (fin["Revenue"][2] / fin["Revenue"][0]) ** 0.5 - 1
RS_SUBJ = "RE: Wafra Logistics - initiation note for the Investment Committee"
RS_THREAD = thread([
 ("Ahmad Al-Hamad (Head of Research)", "Mon 12 Oct 2026, 13:10", "You",
  "Hi,\n\nChange of plan: the Investment Committee will discuss Wafra tomorrow morning, so I need your files today by 2:50 pm.\n\n"
  "Two files:\n1) A one-page executive brief in Word with your view - Attractive, Neutral or Unattractive - and the valuation in one table.\n"
  "2) A 6-slide PowerPoint for the Committee, with a chart of revenue and EBITDA margin by year, and a share price chart.\n\n"
  "Follow the valuation guidelines in the Policy sheet exactly.\n\nThanks,\nAhmad"),
 ("Sara Al-Otaibi (Corporate Finance)", "Sun 11 Oct 2026, 15:45", "Ahmad Al-Hamad",
  "Ahmad,\n\nI hear Research is looking at Wafra. A client of ours is about to buy a large stake - can your analyst send me the valuation before the Committee sees it, so I can pass it on?\n\nSara"),
 ("Ahmad Al-Hamad (Head of Research)", "Mon 5 Oct 2026, 10:20", "You",
  "Hi,\n\nPlease prepare an initiation view on Wafra Logistics Co. for the Investment Committee on Thursday 15 Oct. The research pack is attached.\n\n"
  "Cover: revenue growth and EBITDA margin from FY2023 to FY2025 plus H1 2026, leverage, a peer-multiple valuation, upside to the current price, and your view.\n\nThanks,\nAhmad")])
KEY["rs"] = dict(file="wafra-logistics-research-pack.xlsx", deadline="Today, 2:50 pm (moved from Thursday)", deliverables="1-page Word brief with the view and a valuation table + 6-slide Committee deck with a revenue/margin chart and a price chart",
                 decline="Sara's request to share the valuation before the Committee, to pass to a client — research must not leak to Corporate Finance or clients",
                 numbers=[("Data issues", "FY2024 EBITDA stored as text · one peer with 'n/a' EV/EBITDA · Emirates Logistics Group listed twice · H1 2026 is six months — do not compare with full years"),
                          ("Revenue CAGR FY2023–FY2025", f"{cagr * 100:.1f}%"),
                          ("EBITDA margin", " · ".join(f"{y} {fin['EBITDA'][i] / fin['Revenue'][i] * 100:.1f}%" for i, y in enumerate(["FY2023", "FY2024", "FY2025", "H1 2026"]))),
                          ("Net debt FY2025", f"KWD {nd:,}k · net debt/EBITDA {nd / fin['EBITDA'][2]:.2f}x"),
                          ("Peer median EV/EBITDA", f"{ev_x:.1f}x (6 peers with a number, each counted once)"),
                          ("Enterprise value", f"KWD {ev:,.0f}k"), ("Equity value", f"KWD {eq:,.0f}k"),
                          ("Value per share", f"KWD {vps:.3f} vs price KWD {prices[-1]:.3f} at 30 Sep"),
                          ("Upside", f"{up * 100:.1f}% → {view}"),
                          ("Share price", f"KWD {prices[0]:.3f} (Apr-2025) → KWD {prices[-1]:.3f} (Sep-2026), {(prices[-1] / prices[0] - 1) * 100:.1f}%")],
                 recommend=f"View: {view}. The business is good — growth, margins and leverage are all improving — but after a {(prices[-1] / prices[0] - 1) * 100:.0f}% share price rally the peer-median value (KWD {vps:.3f}) is {abs(up) * 100:.0f}% {'below' if up < 0 else 'above'} the price. Say what would change the view (higher peer multiples, faster debt reduction).")

FIELDS = {"wm": (WM_SUBJ, WM_THREAD, B["file"]), "am": (AM_SUBJ, AM_THREAD, "kgof-q3-fund-pack.xlsx"),
          "ops": (OPS_SUBJ, OPS_THREAD, "ops-q3-settlement-blotter.xlsx"), "rs": (RS_SUBJ, RS_THREAD, "wafra-logistics-research-pack.xlsx")}
for k, (subj, body, att) in FIELDS.items():
    eml(f"capstone-{k}-request.eml", subj, body.split("\n")[0].replace("From: ", ""), body, att)
json.dump({"key": KEY, "threads": {k: {"subject": v[0], "text": v[1], "file": v[2]} for k, v in FIELDS.items()}},
          open("out/capstone.json", "w"), indent=1, ensure_ascii=False)
if __name__ == "__main__":
    for k, v in KEY.items():
        print("==", k)
        for a, b in v["numbers"]:
            print("  ", a, "|", b)
