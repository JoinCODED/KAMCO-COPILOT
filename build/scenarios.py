"""Scenario data for the KAMCO 'AI at Work with Microsoft Copilot' program.
All names, prices and clients are fictional. One security universe, four portfolios:
  murjan  - teaching scenario (decks + trainee lab + Day 2 deliverables)
  waha    - instructor demo scenario (instructor lab)
  bayan   - project version A (Word memo for the Investment Committee)
  sanad   - project version B (PowerPoint deck for a client meeting)
"""
import json, random
from collections import OrderedDict

FX = 0.3065  # USD -> KWD, held constant for the exercise

# id: (name, ticker, issuer, asset_class, sector, region, ccy, p_jun, p_sep)
U = OrderedDict([
 ("ANB",  ("Al-Noor Bank",                 "ANB",   "Al-Noor Bank",        "Equity",       "Banks",           "Kuwait", "KWD", 0.742, 0.811)),
 ("GTB",  ("Gulf Trade Bank",              "GTB",   "Gulf Trade Bank",     "Equity",       "Banks",           "Kuwait", "KWD", 0.512, 0.498)),
 ("BYT",  ("Bayan Telecom",                "BYT",   "Bayan Telecom",       "Equity",       "Telecom",         "Kuwait", "KWD", 0.455, 0.471)),
 ("SDF",  ("Sadaf Logistics",              "SDF",   "Sadaf Logistics",     "Equity",       "Industrials",     "Kuwait", "KWD", 0.268, 0.241)),
 ("JBC",  ("Jaber Cement",                 "JBC",   "Jaber Cement",        "Equity",       "Materials",       "Kuwait", "KWD", 0.190, 0.203)),
 ("FLK",  ("Failaka Foods",                "FLK",   "Failaka Foods",       "Equity",       "Consumer",        "Kuwait", "KWD", 0.336, 0.352)),
 ("NJI",  ("Najd Industrial Holding",      "NJI",   "Najd Industrial",     "Equity",       "Industrials",     "GCC",    "USD", 18.40, 17.25)),
 ("ATLS", ("Atlas Tech Corp",              "ATLS",  "Atlas Tech Corp",     "Equity",       "Technology",      "US",     "USD", 212.50, 238.10)),
 ("NWH",  ("Northwind Health",             "NWH",   "Northwind Health",    "Equity",       "Healthcare",      "US",     "USD", 96.20, 91.80)),
 ("MRDE", ("Meridian Energy",              "MRDE",  "Meridian Energy",     "Equity",       "Energy",          "US",     "USD", 64.75, 69.30)),
 ("CVC",  ("Crestview Consumer",           "CVC",   "Crestview Consumer",  "Equity",       "Consumer",        "US",     "USD", 141.00, 146.60)),
 ("HBRS", ("Harbor Semiconductors",        "HBRS",  "Harbor Semiconductors","Equity",      "Technology",      "US",     "USD", 88.40, 101.90)),
 ("WEQT", ("World Equity Tracker ETF",     "WEQT",  "World Equity Tracker","Equity",       "Diversified",     "Global", "USD", 54.10, 56.35)),
 ("ANBS", ("Al-Noor Bank Sukuk 2029",      "ANB29", "Al-Noor Bank",        "Fixed Income", "Banks",           "Kuwait", "USD", 99.10, 99.60)),
 ("GS31", ("Gulf Sovereign 4.25% 2031",    "GS31",  "Gulf Sovereign",      "Fixed Income", "Government",      "GCC",    "USD", 97.80, 98.90)),
 ("UST30",("US Treasury Note 2030",        "UST30", "US Treasury",         "Fixed Income", "Government",      "US",     "USD", 95.60, 96.75)),
 ("MRDB", ("Meridian Energy 5.1% 2032",    "MRD32", "Meridian Energy",     "Fixed Income", "Energy",          "US",     "USD", 101.20, 100.40)),
 ("GCBF", ("GCC Corporate Bond Fund",      "GCBF",  "GCC Corporate Bond Fund","Fixed Income","Diversified",   "GCC",    "USD", 10.42, 10.51)),
 ("GHR",  ("Gulf Horizon REIT",            "GHR",   "Gulf Horizon REIT",   "Real Estate",  "Real Estate",     "GCC",    "USD", 12.80, 12.15)),
 ("SPF",  ("Salmiya Property Fund",        "SPF",   "Salmiya Property Fund","Real Estate", "Real Estate",     "Kuwait", "KWD", 1.105, 1.118)),
 ("KCD",  ("KWD Call Deposit",             "KWDCASH","Cash",               "Cash",         "Cash",            "Kuwait", "KWD", 1.0, 1.0)),
 ("USMM", ("USD Money Market Fund",        "USDMMF","USD Money Market Fund","Cash",        "Cash",            "Global", "USD", 1.0, 1.0)),
])

# how the raw export spells asset classes (messy on purpose)
MESSY_CLASS = {"Equity": ["Equity", "equities", "EQ", "Equity "],
               "Fixed Income": ["Fixed Income", "FI", "Bonds", "fixed income"],
               "Real Estate": ["Real Estate", "REIT", "real estate"],
               "Cash": ["Cash", "Cash & Deposits", "cash"]}

MANDATE = OrderedDict([("Equity", (0.45, 0.35, 0.55)), ("Fixed Income", (0.30, 0.20, 0.40)),
                       ("Real Estate", (0.10, 0.05, 0.15)), ("Cash", (0.15, 0.05, 0.20))])
ISSUER_LIMIT = 0.10

SCEN = {
 "murjan": dict(client="Al-Murjan Family Office", code="AMFO", seed=11, missing=["NWH", "GHR"], dups=["ATLS", "GTB", "UST30", "FLK"],
   qty={"ANB":560000,"GTB":510000,"BYT":450000,"SDF":900000,"JBC":900000,"FLK":700000,"NJI":15000,"ATLS":4200,"NWH":5600,
        "MRDE":6000,"CVC":3300,"HBRS":7600,"WEQT":14000,"ANBS":3900,"GS31":11000,"UST30":9500,"MRDB":4600,"GCBF":61000,
        "GHR":52000,"SPF":175000,"KCD":205000,"USMM":540000}),
 "waha": dict(client="Al-Waha Family Office", code="AWFO", seed=23, missing=["CVC", "SPF"], dups=["HBRS", "BYT", "GS31"],
   qty={"ANB":180000,"GTB":1000000,"BYT":540000,"SDF":400000,"JBC":500000,"FLK":350000,"NJI":22000,"ATLS":2600,"NWH":6400,
        "MRDE":5200,"CVC":4100,"HBRS":3100,"WEQT":12000,"ANBS":1500,"GS31":10500,"UST30":8800,"MRDB":7400,"GCBF":90000,
        "GHR":15000,"SPF":120000,"KCD":410000,"USMM":620000}),
 "bayan": dict(client="Al-Bayan Holding", code="ABH", seed=37, missing=["MRDE", "SPF"], dups=["ANB", "NWH", "GCBF"],
   qty={"ANB":260000,"GTB":300000,"BYT":450000,"SDF":500000,"JBC":400000,"FLK":420000,"NJI":12000,"ATLS":3500,"NWH":3900,
        "MRDE":6100,"CVC":2700,"HBRS":4300,"WEQT":8000,"ANBS":2100,"GS31":9000,"UST30":8000,"MRDB":2600,"GCBF":30000,
        "GHR":105000,"SPF":260000,"KCD":120000,"USMM":300000}),
 "sanad": dict(client="Dar Al-Sanad Trust", code="DAST", seed=51, missing=["ATLS", "GCBF"], dups=["SDF", "MRDB", "WEQT"],
   qty={"ANB":150000,"GTB":250000,"BYT":300000,"SDF":350000,"JBC":500000,"FLK":300000,"NJI":8000,"ATLS":3600,"NWH":2400,
        "MRDE":3800,"CVC":2200,"HBRS":2900,"WEQT":15000,"ANBS":2600,"GS31":7300,"UST30":6900,"MRDB":4400,"GCBF":52000,
        "GHR":30000,"SPF":95000,"KCD":520000,"USMM":1150000}),
}


def compute(key):
    s = SCEN[key]
    rows = []
    for sid, (name, tic, issuer, ac, sec, reg, ccy, pj, ps) in U.items():
        q = s["qty"][sid]
        fx = 1.0 if ccy == "KWD" else FX
        rows.append(dict(id=sid, name=name, ticker=tic, issuer=issuer, ac=ac, sector=sec, region=reg, ccy=ccy, qty=q,
                         pj=pj, ps=ps, mv_jun=q * pj * fx, mv_sep=q * ps * fx))
    tot_sep = sum(r["mv_sep"] for r in rows)
    tot_jun = sum(r["mv_jun"] for r in rows)
    alloc = OrderedDict((a, sum(r["mv_sep"] for r in rows if r["ac"] == a) / tot_sep) for a in MANDATE)
    nc = [r for r in rows if r["ac"] != "Cash"]
    issuers = {}
    for r in nc:
        issuers[r["issuer"]] = issuers.get(r["issuer"], 0) + r["mv_sep"]
    iss = sorted(((k, v / tot_sep) for k, v in issuers.items()), key=lambda x: -x[1])
    contrib = sorted(((r["name"], r["mv_sep"] - r["mv_jun"]) for r in rows), key=lambda x: -x[1])
    breaches = [a for a, (t, lo, hi) in MANDATE.items() if not (lo <= alloc[a] <= hi)]
    issuer_breaches = [(k, v) for k, v in iss if v > ISSUER_LIMIT]
    return dict(rows=rows, tot_sep=tot_sep, tot_jun=tot_jun, ret=tot_sep / tot_jun - 1, alloc=alloc, issuers=iss,
                contrib=contrib, breaches=breaches, issuer_breaches=issuer_breaches)


def report(key):
    c = compute(key)
    print("==", key, SCEN[key]["client"])
    print("  total sep KWD {:,.0f}  jun {:,.0f}  Q3 return {:.2%}".format(c["tot_sep"], c["tot_jun"], c["ret"]))
    for a, w in c["alloc"].items():
        t, lo, hi = MANDATE[a]
        print("  {:13s} {:6.1%}  range {:.0%}-{:.0%} {}".format(a, w, lo, hi, "BREACH" if a in c["breaches"] else ""))
    print("  top issuers:", [(k, round(v * 100, 2)) for k, v in c["issuers"][:4]])
    print("  top contrib:", [(k, round(v)) for k, v in c["contrib"][:3]], " bottom:", [(k, round(v)) for k, v in c["contrib"][-3:]])
    return c


if __name__ == "__main__":
    for k in SCEN:
        report(k)
