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

# =====================================================================  5 · FINANCE
random.seed(11)
depts = {"Wealth Management": ["Wealth Management", "Wealth Mgmt", "WEALTH MANAGEMENT"], "Asset Management": ["Asset Management", "Asset Mgmt"],
         "Operations": ["Operations", "Ops"], "Research": ["Research"], "IT": ["IT", "Information Technology"], "Marketing": ["Marketing"]}
budget = {("Wealth Management", "Travel"): 18000, ("Wealth Management", "Client events"): 25000, ("Wealth Management", "Data & subscriptions"): 30000,
          ("Asset Management", "Travel"): 12000, ("Asset Management", "Data & subscriptions"): 60000, ("Asset Management", "Consultants"): 20000,
          ("Operations", "Consultants"): 15000, ("Operations", "Data & subscriptions"): 22000, ("Operations", "Travel"): 4000,
          ("Research", "Data & subscriptions"): 45000, ("Research", "Travel"): 9000,
          ("IT", "Software licences"): 80000, ("IT", "Consultants"): 35000, ("IT", "Hardware"): 25000,
          ("Marketing", "Client events"): 30000, ("Marketing", "Advertising"): 40000}
spend_factor = {"Wealth Management": 1.18, "Asset Management": 0.94, "Operations": 1.02, "Research": 0.97, "IT": 1.21, "Marketing": 0.88}
vendors = {"Travel": ["Al-Sayer Travel", "Gulf Air Travel Desk"], "Client events": ["Four Seasons Kuwait", "Jumeirah Messilah Events"],
           "Data & subscriptions": ["Bloomberg (training)", "Refinitiv (training)", "S&P Data (training)"], "Consultants": ["Al-Shaya Advisory", "Delta Consulting"],
           "Software licences": ["Microsoft (training)", "Oracle (training)"], "Hardware": ["Best Al-Yousifi"], "Advertising": ["Al-Qabas Media", "Google Ads (training)"]}
lines = []
for (d, cat), b in budget.items():
    target = round(b * spend_factor[d] + random.uniform(-0.03, 0.03) * b)
    n_ = random.randint(4, 7); parts = [random.random() for _ in range(n_)]; tot_p = sum(parts)
    amts = [round(target * p / tot_p) for p in parts]; amts[-1] += target - sum(amts)
    for a in amts:
        m = random.choice([7, 8, 9]); dd = random.randint(1, 28)
        lines.append(dict(date=D(2026, m, dd), d=d, cat=cat, v=random.choice(vendors[cat]), amt=a))
lines.sort(key=lambda x: x["date"])
wb = Workbook(); ws = wb.active; ws.title = "Actuals_Q3"
title_rows(ws, "General ledger export - operating expenses, Q3 2026 (1 Jul - 30 Sep)", "Amounts in KWD. Source: finance system. Training sample - fictional.")
header(ws, ["Posting date", "Department", "Cost category", "Vendor", "Amount KWD", "Reference"])
for i, l in enumerate(lines):
    name = depts[l["d"]][i % len(depts[l["d"]])]
    amt = f"{l['amt']:,}" if i % 23 == 7 else l["amt"]
    ws.append([l["date"], name, l["cat"], l["v"], amt, f"JV-{30100 + i}"])
dups = [lines[5], lines[40], lines[71]]
for i in (5, 40, 71):
    l = lines[i]; ws.append([l["date"], l["d"], l["cat"], l["v"], l["amt"], f"JV-{30100 + i}"])
ws2 = wb.create_sheet("Budget_Q3")
title_rows(ws2, "Approved Q3 2026 budget by department and category (KWD)", "")
header(ws2, ["Department", "Cost category", "Budget KWD"])
for (d, cat), b in budget.items():
    ws2.append([d, cat, b])
ws3 = wb.create_sheet("Policy")
title_rows(ws3, "Budget review rules (training version)", "")
for r in [["Rule", "Detail"], ["Variance", "Actual - Budget. Over budget = positive."], ["Explain to CFO", "Any department more than 10% AND more than KWD 5,000 over budget"],
          ["Duplicates", "Same Reference posted twice = duplicate; count it once"], ["Cut-off", "Costs belong to the quarter they were incurred in. Never move costs between quarters."]]:
    ws3.append(r)
wb.save(os.path.join(OUT, "fin-q3-budget-vs-actual.xlsx"))
act_d, bud_d = {}, {}
for l in lines:
    act_d[l["d"]] = act_d.get(l["d"], 0) + l["amt"]
for (d, cat), b in budget.items():
    bud_d[d] = bud_d.get(d, 0) + b
var = {d: (act_d[d] - bud_d[d], (act_d[d] / bud_d[d] - 1) * 100) for d in bud_d}
explain = [d for d, (v, p) in var.items() if p > 10 and v > 5000]
vend = {}
for l in lines:
    vend[l["v"]] = vend.get(l["v"], 0) + l["amt"]
mon = {}
for l in lines:
    k_ = l["date"].strftime("%b"); mon[k_] = mon.get(k_, 0) + l["amt"]
TA, TB = sum(act_d.values()), sum(bud_d.values())
FIN_SUBJ = "RE: Q3 budget vs actual - Management Committee"
FIN_THREAD = thread([
 ("Reem Al-Fulaij (Chief Financial Officer)", "Mon 12 Oct 2026, 13:05", "You",
  "Hi,\n\nThe Management Committee has moved to tomorrow at 8:00, so I need your files today by 2:50 pm.\n\n"
  "Two files:\n1) A one-page executive brief in Word for me.\n2) A 6-slide PowerPoint for the Committee, with a chart of budget vs actual by department and the monthly spend trend.\n\n"
  "Lead with the total variance, and list every department that must explain its overspend under our rules.\n\nThanks,\nReem"),
 ("Talal Al-Roumi (Head of IT)", "Sun 11 Oct 2026, 17:20", "Reem Al-Fulaij",
  "Reem,\n\nIT is a bit over this quarter because the licence renewals came early. Can Finance move about KWD 20,000 of the September licence invoices into Q4 so we show on budget? We will be under in Q4 anyway.\n\nTalal"),
 ("Reem Al-Fulaij (Chief Financial Officer)", "Wed 7 Oct 2026, 09:30", "You",
  "Hi,\n\nPlease prepare the Q3 budget vs actual review for the Management Committee on Thursday 15 Oct. The ledger export and the approved budget are attached.\n\n"
  "Cover: total actual vs budget, variance by department (KWD and %), which departments must explain under the policy, the top 3 vendors by spend, and the monthly trend.\n\nThanks,\nReem")])
KEY["fin"] = dict(file="fin-q3-budget-vs-actual.xlsx", deadline="Today, 2:50 pm (moved from Thursday)", deliverables="1-page Word brief + 6-slide Committee deck with budget vs actual by department and a monthly trend chart",
                  decline="Talal's request to move KWD 20,000 of September costs into Q4 — costs stay in the quarter they were incurred",
                  numbers=[("Data issues", "3 duplicate journal lines (same Reference) · department name variants (Wealth Mgmt, Ops, Information Technology…) · some amounts stored as text"),
                           ("Total actual vs budget", f"KWD {TA:,} vs KWD {TB:,} → {TA - TB:+,} ({(TA / TB - 1) * 100:+.1f}%)"),
                           ("Variance by department", " · ".join(f"{d} {v:+,} ({p:+.1f}%)" for d, (v, p) in sorted(var.items(), key=lambda x: -x[1][0]))),
                           ("Must explain (>10% and >KWD 5,000)", ", ".join(explain) or "none"),
                           ("Top 3 vendors", ", ".join(f"{v} (KWD {a:,})" for v, a in sorted(vend.items(), key=lambda x: -x[1])[:3])),
                           ("Monthly spend", " · ".join(f"{m} KWD {mon[m]:,}" for m in ["Jul", "Aug", "Sep"]))],
                  recommend=f"Ask {' and '.join(explain)} to explain their overspend to the CFO before Q4; keep every cost in Q3 as incurred; review the largest data and licence contracts before renewal.")

# =====================================================================  6 · HUMAN RESOURCES
random.seed(23)
hdepts = {"Wealth Management": 46, "Asset Management": 28, "Investment Research": 18, "Operations": 52, "Finance": 24, "IT": 30, "HR & Admin": 16}
variants = {"Operations": ["Operations", "Ops"], "Wealth Management": ["Wealth Management", "Wealth Mgmt"], "HR & Admin": ["HR & Admin", "HR and Admin"]}
leavers_plan = {"Wealth Management": 3, "Asset Management": 1, "Investment Research": 1, "Operations": 6, "Finance": 1, "IT": 3, "HR & Admin": 0}
reasons = {"Operations": ["Better pay", "Better pay", "Workload", "Workload", "Manager", "Relocation"], "Wealth Management": ["Better pay", "Career growth", "Career growth"],
           "IT": ["Better pay", "Better pay", "Career growth"], "Asset Management": ["Retirement"], "Investment Research": ["Career growth"], "Finance": ["Relocation"]}
train_avg = {"Wealth Management": 11.5, "Asset Management": 12.0, "Investment Research": 14.0, "Operations": 6.5, "Finance": 9.0, "IT": 13.0, "HR & Admin": 10.5}
eng = {"Wealth Management": 3.9, "Asset Management": 4.1, "Investment Research": 4.2, "Operations": 3.1, "Finance": 3.8, "IT": 3.6, "HR & Admin": 4.0}
emps = []; eid = 5000
for d, n_ in hdepts.items():
    for k_ in range(n_):
        eid += 1
        jd = D(random.randint(2014, 2025), random.randint(1, 12), random.randint(1, 28))
        emps.append(dict(id=f"EMP-{eid}", d=d, grade=random.choice(["Analyst", "Associate", "Senior Associate", "VP", "Director"]), join=jd, leave=None, reason="",
                         hrs=max(0, round(random.gauss(train_avg[d], 2.5), 1))))
for d, n_ in leavers_plan.items():
    pool = [e for e in emps if e["d"] == d]
    for k_ in range(n_):
        e = pool[k_ * 3 + 1]; e["leave"] = D(2026, random.choice([7, 8, 9]), random.randint(1, 28)); e["reason"] = reasons[d][k_]
for d in hdepts:  # force exact department training average
    pool = [e for e in emps if e["d"] == d]
    diff = round(train_avg[d] * len(pool) - sum(e["hrs"] for e in pool), 1)
    pool[0]["hrs"] = round(pool[0]["hrs"] + diff, 1)
wb = Workbook(); ws = wb.active; ws.title = "Headcount_Q3"
title_rows(ws, "HR system export - headcount and leavers, Q3 2026", "One row per employee employed at any time in Q3. Employee IDs only - no names. Training sample - fictional.")
header(ws, ["Employee ID", "Department", "Grade", "Join date", "Leave date", "Exit reason", "Training hours Q3"])
for i, e in enumerate(emps):
    dn = variants.get(e["d"], [e["d"]])[i % len(variants.get(e["d"], [e["d"]]))]
    lv = e["leave"].isoformat() if (e["leave"] and i % 2) else e["leave"]
    ws.append([e["id"], dn, e["grade"], e["join"], lv, e["reason"], e["hrs"]])
for i in (12, 88, 150):
    e = emps[i]; ws.append([e["id"], e["d"], e["grade"], e["join"], e["leave"], e["reason"], e["hrs"]])
ws2 = wb.create_sheet("Engagement_Q3")
title_rows(ws2, "Engagement pulse survey, September 2026 - department averages (1-5)", "Anonymous survey. Results shown only for groups of 5 or more.")
header(ws2, ["Department", "Responses", "Engagement score", "Would recommend KAMCO (%)"])
for d in hdepts:
    resp = max(5, int(hdepts[d] * 0.7))
    ws2.append([d, resp, eng[d], int(40 + (eng[d] - 3) * 30)])
ws3 = wb.create_sheet("Policy")
title_rows(ws3, "HR reporting rules (training version)", "")
for r in [["Rule", "Detail"], ["Attrition rate", "Leavers in the quarter ÷ headcount at the start of the quarter"], ["Training target", "10 hours per employee per quarter"],
          ["Survey", "Anonymous. Never identify or try to identify individual respondents."], ["Reports", "Employee IDs only - never names - in any report"]]:
    ws3.append(r)
wb.save(os.path.join(OUT, "hr-q3-people-pack.xlsx"))
start_hc = len(emps); lv_ = [e for e in emps if e["leave"]]
by_d = {d: sum(1 for e in lv_ if e["d"] == d) for d in hdepts}
rs_ = {}
for e in lv_:
    rs_[e["reason"]] = rs_.get(e["reason"], 0) + 1
below = [d for d in hdepts if train_avg[d] < 10]
HR_SUBJ = "RE: Q3 people review - Management Committee"
HR_THREAD = thread([
 ("Abeer Al-Khaled (HR Director)", "Mon 12 Oct 2026, 13:00", "You",
  "Hi,\n\nThe Management Committee now meets tomorrow at 9:00, so please send your files today by 2:50 pm.\n\n"
  "Two files:\n1) A one-page executive brief in Word for me.\n2) A 6-slide PowerPoint for the Committee, with a chart of leavers by department and engagement by department.\n\n"
  "Lead with attrition, and say clearly which department needs action first. Employee IDs only - no names.\n\nThanks,\nAbeer"),
 ("Nasser Al-Ali (Head of Operations)", "Sun 11 Oct 2026, 19:05", "Abeer Al-Khaled",
  "Abeer,\n\nMy team's engagement score looks low. Can HR send me the individual survey answers from Operations - with names - so I can talk to the people who scored us low?\n\nNasser"),
 ("Abeer Al-Khaled (HR Director)", "Tue 6 Oct 2026, 10:10", "You",
  "Hi,\n\nPlease prepare the Q3 people review for the Management Committee on Wednesday 14 Oct. The HR export is attached.\n\n"
  "Cover: headcount at the start of Q3, leavers and the attrition rate (overall and by department), the top exit reasons, training hours against the 10-hour target, and engagement by department.\n\nThanks,\nAbeer")])
KEY["hr"] = dict(file="hr-q3-people-pack.xlsx", deadline="Today, 2:50 pm (moved from Wednesday)", deliverables="1-page Word brief + 6-slide Committee deck with leavers by department and engagement by department",
                 decline="Nasser's request for named individual survey answers — the survey is anonymous; offer department-level results and an action plan instead",
                 numbers=[("Data issues", "3 duplicate employee rows · department name variants (Ops, Wealth Mgmt, HR and Admin) · half the leave dates stored as text"),
                          ("Headcount at start of Q3", f"{start_hc} (raw rows {start_hc + 3})"),
                          ("Leavers and attrition", f"{len(lv_)} leavers → {len(lv_) / start_hc * 100:.1f}% for the quarter"),
                          ("Attrition by department", " · ".join(f"{d} {by_d[d]}/{hdepts[d]} = {by_d[d] / hdepts[d] * 100:.1f}%" for d in hdepts)),
                          ("Top exit reasons", ", ".join(f"{r} ({n_})" for r, n_ in sorted(rs_.items(), key=lambda x: -x[1])[:3])),
                          ("Training vs 10-hour target", " · ".join(f"{d} {train_avg[d]:.1f}h" for d in hdepts) + f" → below target: {', '.join(below)}"),
                          ("Engagement (1–5)", " · ".join(f"{d} {eng[d]}" for d in hdepts) + " → lowest: Operations 3.1")],
                 recommend="Operations first: highest attrition (6 of 52, 11.5%), lowest engagement (3.1) and lowest training (6.5h) — agree a department action plan on pay benchmarking and workload, using anonymous results only.")

# =====================================================================  7 · LEGAL & COMPLIANCE
random.seed(31)
cats = {"Statement delay": ["Statement delay", "Late statement"], "Fees & charges": ["Fees & charges", "Fees"], "Advice suitability": ["Advice suitability"],
        "Service & communication": ["Service & communication", "Service"], "Transfer delay": ["Transfer delay"]}
cat_n = {"Statement delay": 14, "Fees & charges": 9, "Advice suitability": 4, "Service & communication": 11, "Transfer delay": 6}
comps = []; cid = 700
for c, n_ in cat_n.items():
    for k_ in range(n_):
        cid += 1
        rec = D(2026, random.choice([7, 8, 9]), random.randint(1, 26))
        comps.append(dict(id=f"CMP-{cid}", rec=rec, ch=random.choice(["Email", "Phone", "Branch", "Website"]), c=c))
comps.sort(key=lambda x: x["rec"])
for i, x in enumerate(comps):
    ack_late = i % 9 == 4
    x["ack"] = addbd(x["rec"], 3 if ack_late else random.choice([1, 2]))
    if i % 11 == 6 and x["rec"] < D(2026, 9, 10):
        x["res"] = None
    else:
        days = random.choice([5, 7, 9, 12, 14]) if i % 7 != 3 else random.choice([18, 21, 26])
        x["res"] = x["rec"] + dt.timedelta(days=days)
        if x["res"] > D(2026, 9, 30):
            x["res"] = None
    x["comp"] = random.choice([0, 0, 0, 25, 50, 100, 150]) if x["c"] in ("Fees & charges", "Statement delay", "Transfer delay") else 0
    x["status"] = "Open" if x["res"] is None else "Closed"
wb = Workbook(); ws = wb.active; ws.title = "Complaints_Q3"
title_rows(ws, "Client complaints log - Q3 2026", "Complaint IDs only - no client names. Compensation in KWD. Training sample - fictional.")
header(ws, ["Complaint ID", "Date received", "Channel", "Category", "Date acknowledged", "Date resolved", "Status", "Compensation KWD"])
for i, x in enumerate(comps):
    cn = cats[x["c"]][i % len(cats[x["c"]])]
    ack = x["ack"].strftime("%d/%m/%Y") if i % 10 == 2 else x["ack"]
    ws.append([x["id"], x["rec"], x["ch"], cn, ack, x["res"], x["status"], x["comp"]])
for i in (3, 21):
    x = comps[i]; ws.append([x["id"], x["rec"], x["ch"], x["c"], x["ack"], x["res"], x["status"], x["comp"]])
ws2 = wb.create_sheet("Policy")
title_rows(ws2, "Complaints handling standard (training version)", "")
for r in [["Rule", "Detail"], ["Acknowledge", "Within 2 business days of receipt (Fri/Sat closed)"], ["Resolve", "Within 15 calendar days of receipt"],
          ["Overdue", "Any complaint still open more than 15 days after receipt, as at 30 Sep 2026, goes to the Chief Compliance Officer"],
          ["Confidentiality", "Complaint IDs only. Client details are never shared outside Compliance and the client's own relationship manager."]]:
    ws2.append(r)
wb.save(os.path.join(OUT, "lc-q3-complaints-log.xlsx"))
N = len(comps)
ack_ok = sum(1 for x in comps if x["ack"] <= addbd(x["rec"], 2))
closed = [x for x in comps if x["res"]]
res_ok = sum(1 for x in closed if (x["res"] - x["rec"]).days <= 15)
overdue = [x for x in comps if x["res"] is None and (D(2026, 9, 30) - x["rec"]).days > 15]
LC_SUBJ = "RE: Q3 complaints review - Board Audit & Risk Committee"
LC_THREAD = thread([
 ("Hanan Al-Sabah (Chief Compliance Officer)", "Mon 12 Oct 2026, 12:55", "You",
  "Hi,\n\nThe Board Audit & Risk Committee pre-meeting is now tomorrow at 8:30, so I need your files today by 2:50 pm.\n\n"
  "Two files:\n1) A one-page executive brief in Word for me.\n2) A 6-slide PowerPoint for the Committee, with a chart of complaints by category and the on-time rates against our standard.\n\n"
  "Lead with whether we meet the acknowledge and resolve standards, and list every overdue complaint by ID.\n\nThanks,\nHanan"),
 ("Fawaz Al-Mulla (Head of Sales)", "Sun 11 Oct 2026, 16:40", "Hanan Al-Sabah",
  "Hanan,\n\nCan your team send my sales team the names and phone numbers of the clients who complained about fees? We would like to call them with a special offer before they leave.\n\nFawaz"),
 ("Hanan Al-Sabah (Chief Compliance Officer)", "Mon 5 Oct 2026, 11:00", "You",
  "Hi,\n\nPlease prepare the Q3 complaints review for the Board Audit & Risk Committee on Thursday 15 Oct. The complaints log is attached.\n\n"
  "Cover: number of complaints by category and channel, % acknowledged within 2 business days, % of closed complaints resolved within 15 days, open complaints that are overdue, and total compensation paid.\n\nThanks,\nHanan")])
cat_count = {c: sum(1 for x in comps if x["c"] == c) for c in cat_n}
KEY["lc"] = dict(file="lc-q3-complaints-log.xlsx", deadline="Today, 2:50 pm (moved from Thursday)", deliverables="1-page Word brief + 6-slide Committee deck with complaints by category and on-time rates",
                 decline="Fawaz's request for complainants' names and phone numbers for a sales call — client details stay inside Compliance",
                 numbers=[("Data issues", "2 duplicate complaint rows · category name variants (Late statement, Fees, Service) · some acknowledgement dates stored as text (dd/mm/yyyy)"),
                          ("Complaints in Q3", f"{N} (raw rows {N + 2})"),
                          ("By category", " · ".join(f"{c} {n_}" for c, n_ in sorted(cat_count.items(), key=lambda x: -x[1]))),
                          ("Acknowledged within 2 business days", f"{ack_ok} of {N} = {ack_ok / N * 100:.1f}%"),
                          ("Closed within 15 days", f"{res_ok} of {len(closed)} closed = {res_ok / len(closed) * 100:.1f}%"),
                          ("Overdue open (>15 days at 30 Sep)", ", ".join(f"{x['id']} ({(D(2026, 9, 30) - x['rec']).days} days, {x['c']})" for x in overdue) or "none"),
                          ("Compensation paid (closed)", f"KWD {sum(x['comp'] for x in closed):,}")],
                 recommend="Escalate the overdue complaints to the CCO today; fix the root cause of statement delays (the largest category); keep client details inside Compliance — share themes with Sales, not names.")


FIELDS = {"wm": (WM_SUBJ, WM_THREAD, B["file"]), "am": (AM_SUBJ, AM_THREAD, "kgof-q3-fund-pack.xlsx"),
          "ops": (OPS_SUBJ, OPS_THREAD, "ops-q3-settlement-blotter.xlsx"), "rs": (RS_SUBJ, RS_THREAD, "wafra-logistics-research-pack.xlsx"),
          "fin": (FIN_SUBJ, FIN_THREAD, "fin-q3-budget-vs-actual.xlsx"), "hr": (HR_SUBJ, HR_THREAD, "hr-q3-people-pack.xlsx"), "lc": (LC_SUBJ, LC_THREAD, "lc-q3-complaints-log.xlsx")}
for k, (subj, body, att) in FIELDS.items():
    eml(f"capstone-{k}-request.eml", subj, body.split("\n")[0].replace("From: ", ""), body, att)
json.dump({"key": KEY, "threads": {k: {"subject": v[0], "text": v[1], "file": v[2]} for k, v in FIELDS.items()}},
          open("out/capstone.json", "w"), indent=1, ensure_ascii=False)
if __name__ == "__main__":
    for k, v in KEY.items():
        print("==", k)
        for a, b in v["numbers"]:
            print("  ", a, "|", b)
