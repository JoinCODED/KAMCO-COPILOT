import json, re, os, importlib
import deckkit, deckkit2
deckkit2.install({
    "pre": "https://portal.joincoded.com/sv/kamco-copilot-map-test-pre-day-1",
    "post": "https://portal.joincoded.com/sv/kamco-copilot-map-test-post-day-2",
    "sat": "https://portal.joincoded.com/sv/kamco-copilot-end-of-program-satisfaction-survey",
})

EX = deckkit.EX
OUTP = "out/site"; OUTF = "out/facilitator"
os.makedirs(OUTP, exist_ok=True); os.makedirs(OUTF, exist_ok=True)

TOPICS = {
 1: {"open": "Opening", "t1": "Block 1 · AI, LLMs & Copilot", "t2": "Block 2 · Prompting with CTFT", "t3": "Block 3 · Read the request in Outlook",
     "t4": "Block 4 · Excel: clean the data", "t5": "Block 5 · Excel: find the story", "close": "Hands-on, recap & close"},
 2: {"open": "Opening", "t1": "Topic 1 · Memo or deck? Then Word", "t2": "Topic 2 · PowerPoint", "t3": "Topic 3 · Reply and review",
     "t4": "Topic 4 · From manual to agent · Project", "close": "MAP test, certificates & close"},
}
KIND = {"open": "Open", "story": "Story", "analogy": "Analogy", "term": "The term", "check": "Your call", "demo": "Live demo", "case": "Real case", "pause": "Pause", "close": "Wrap"}


def notes_page(day, notes):
    src = open(EX + "presenter-notes.html", encoding="utf-8").read()
    a = src.index("const TOPICS="); b = src.index("];", src.index("const S=[")) + 2
    js = "const TOPICS=" + json.dumps(TOPICS[day], ensure_ascii=False) + ";\nconst KIND=" + json.dumps(KIND) + ";\nconst S=" + json.dumps(notes, ensure_ascii=False, indent=0) + ";"
    out = src[:a] + js + src[b:]
    out = re.sub(r"<title>.*?</title>", "<title>Day %d · Presenter Notes — KAMCO Copilot</title>" % day, out)
    out = out.replace("Day&nbsp;2 · <b>Presenter Notes</b>", "Day&nbsp;%d · <b>Presenter Notes</b>" % day)
    out = out.replace("kibs_d2_notes", "kamco_d%d_notes" % day)
    out = re.sub(r'<span id="pt">\d+</span>', '<span id="pt">%d</span>' % len(notes), out)
    return out


def build(day):
    mod = importlib.import_module("content_day%d" % day)
    slides = [h for h, n in mod.S]
    notes = [n for h, n in mod.S]
    html = deckkit2.page("Day %d · AI at Work with Microsoft Copilot — CODED × KAMCO Invest" % day, "coded-kamco-day-%d.html" % day, slides)
    open(os.path.join(OUTP, "coded-kamco-day-%d-deck.html" % day), "w", encoding="utf-8").write(html)
    open(os.path.join(OUTF, "coded-kamco-day-%d-notes.html" % day), "w", encoding="utf-8").write(notes_page(day, notes))
    json.dump(dict(checks=mod.CHECKS, notes=notes, n=len(slides)), open("out/deck%d.json" % day, "w"), indent=1, ensure_ascii=False)
    print("day", day, "slides", len(slides), "checks", len(mod.CHECKS))


if __name__ == "__main__":
    build(1); build(2)
