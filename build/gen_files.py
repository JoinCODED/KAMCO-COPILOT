"""Generate the trainee-facing scenario files (messy custody exports, emails, house view) + answers.json"""
import json, random, datetime, os
from email.message import EmailMessage
from email.utils import format_datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from docx import Document
from docx.shared import Pt
from scenarios import SCEN, U, FX, MANDATE, ISSUER_LIMIT, MESSY_CLASS, compute

OUT = "out/files"
os.makedirs(OUT, exist_ok=True)
ARIAL = "Arial"


def messy_export(key):
    s = SCEN[key]; c = compute(key); rnd = random.Random(s["seed"])
    rows = []
    for i, r in enumerate(c["rows"]):
        rows.append(dict(r, hid="%s-%04d" % (s["code"], 101 + i)))
    rnd.shuffle(rows)
    # duplicates: exact copies inserted later in the list
    dup_ids = s["dups"]
    out = list(rows)
    for sid in dup_ids:
        src = next(r for r in rows if r["id"] == sid)
        pos = rnd.randint(len(out) // 2, len(out))
        out.insert(pos, dict(src, _dup=True))
    # decide messy presentation per *holding* so duplicates stay exact copies
    style = {}
    for r in rows:
        style[r["id"]] = dict(
            ac=rnd.choice(MESSY_CLASS[r["ac"]]),
            tick=r["ticker"] + (" " if rnd.random() < 0.25 else ""),
            qty_text=rnd.random() < 0.18,
            date=rnd.choice(["date", "text_dmy", "text_iso"]))
    wb = Workbook(); ws = wb.active; ws.title = "Holdings_Export"
    ws["A1"] = "CUSTODY HOLDINGS EXPORT - %s (%s) - Discretionary mandate" % (s["client"], s["code"])
    ws["A2"] = "Generated 01/10/2026 07:42 by custody system. TRAINING DATA - all names, prices and clients are fictional."
    ws["A1"].font = Font(name=ARIAL, bold=True, size=12); ws["A2"].font = Font(name=ARIAL, italic=True, size=9, color="666666")
    hdr = ["Holding ID", "Security", "Ticker", "Issuer", "Asset Class", "Sector", "Region", "Currency", "Quantity",
           "Price 30-Jun-2026", "Price 30-Sep-2026", "Price Date"]
    for j, h in enumerate(hdr, 1):
        cell = ws.cell(row=4, column=j, value=h); cell.font = Font(name=ARIAL, bold=True); cell.fill = PatternFill("solid", fgColor="D9D9D9")
    for i, r in enumerate(out):
        st = style[r["id"]]; rr = 5 + i
        qty = "{:,}".format(r["qty"]) if st["qty_text"] else r["qty"]
        ps = None if r["id"] in s["missing"] else r["ps"]
        if st["date"] == "date":
            pdv = datetime.date(2026, 9, 30)
        elif st["date"] == "text_dmy":
            pdv = "30/09/2026"
        else:
            pdv = "2026-09-30"
        vals = [r["hid"], r["name"], st["tick"], r["issuer"], st["ac"], r["sector"], r["region"], r["ccy"], qty, r["pj"], ps, pdv]
        for j, v in enumerate(vals, 1):
            cell = ws.cell(row=rr, column=j, value=v); cell.font = Font(name=ARIAL)
            if j == 12 and isinstance(v, datetime.date):
                cell.number_format = "dd/mm/yyyy"
    widths = [13, 30, 9, 24, 14, 13, 9, 9, 12, 16, 16, 12]
    for j, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    # price list
    pl = wb.create_sheet("Price_List")
    for j, h in enumerate(["Ticker", "Security", "Currency", "Price 30-Sep-2026", "Source"], 1):
        cell = pl.cell(row=1, column=j, value=h); cell.font = Font(name=ARIAL, bold=True); cell.fill = PatternFill("solid", fgColor="D9D9D9")
    for i, (sid, u) in enumerate(U.items(), 2):
        for j, v in enumerate([u[1], u[0], u[6], u[8], "Pricing vendor close, 30-Sep-2026 (fictional)"], 1):
            pl.cell(row=i, column=j, value=v).font = Font(name=ARIAL)
    for j, w in enumerate([10, 30, 10, 18, 44], 1):
        pl.column_dimensions[get_column_letter(j)].width = w
    fx = wb.create_sheet("FX_Rates")
    for j, h in enumerate(["Currency", "Rate to KWD", "Note"], 1):
        cell = fx.cell(row=1, column=j, value=h); cell.font = Font(name=ARIAL, bold=True); cell.fill = PatternFill("solid", fgColor="D9D9D9")
    for i, row in enumerate([["KWD", 1, "Base currency"], ["USD", FX, "Held constant for 30-Jun and 30-Sep in this exercise"]], 2):
        for j, v in enumerate(row, 1):
            fx.cell(row=i, column=j, value=v).font = Font(name=ARIAL)
    fx.column_dimensions["C"].width = 52
    md = wb.create_sheet("Mandate")
    for j, h in enumerate(["Asset Class", "Target", "Minimum", "Maximum"], 1):
        cell = md.cell(row=1, column=j, value=h); cell.font = Font(name=ARIAL, bold=True); cell.fill = PatternFill("solid", fgColor="D9D9D9")
    for i, (a, (t, lo, hi)) in enumerate(MANDATE.items(), 2):
        for j, v in enumerate([a, t, lo, hi], 1):
            cell = md.cell(row=i, column=j, value=v); cell.font = Font(name=ARIAL)
            if j > 1: cell.number_format = "0%"
    notes = ["Single-issuer limit: no issuer above 10% of total portfolio value (equity and fixed income from the same issuer are added together; cash is excluded).",
             "Weights are measured on market value in KWD at 30-Sep-2026.",
             "Q3 change = market value at 30-Sep-2026 minus market value at 30-Jun-2026. Quantities did not change during Q3."]
    for i, n in enumerate(notes, 8):
        md.cell(row=i, column=1, value=n).font = Font(name=ARIAL, italic=True)
    md.column_dimensions["A"].width = 16
    fname = "%s-q3-custody-export.xlsx" % s["code"].lower()
    wb.save(os.path.join(OUT, fname))
    return fname, len(out)


def answers(key, raw_rows, fname):
    c = compute(key); s = SCEN[key]
    tops = c["contrib"]
    return dict(client=s["client"], code=s["code"], file=fname, raw_rows=raw_rows, duplicates=len(s["dups"]),
                holdings=len(U), missing_prices=len(s["missing"]),
                missing_tickers=[U[m][1] for m in s["missing"]],
                total_sep=round(c["tot_sep"]), total_jun=round(c["tot_jun"]), q3_change=round(c["tot_sep"] - c["tot_jun"]),
                q3_return_pct=round(c["ret"] * 100, 2),
                alloc_pct={a: round(w * 100, 1) for a, w in c["alloc"].items()},
                breaches=c["breaches"],
                issuer_top=[(k, round(v * 100, 2)) for k, v in c["issuers"][:3]],
                issuer_breaches=[(k, round(v * 100, 2)) for k, v in c["issuer_breaches"]],
                top3=[(k, round(v)) for k, v in tops[:3]], bottom3=[(k, round(v)) for k, v in tops[-3:]][::-1],
                wrong_if_dups_kept=round(c["tot_sep"] + sum(r["mv_sep"] for r in c["rows"] if r["id"] in s["dups"])))


if __name__ == "__main__":
    A = {}
    for k in SCEN:
        f, n = messy_export(k)
        A[k] = answers(k, n, f)
    json.dump(A, open("out/answers.json", "w"), indent=1)
    print(json.dumps(A, indent=1))
