# KAMCO Invest — AI at Work with Microsoft Copilot

CODED × KAMCO Invest, Program 2 · Sun 11 – Mon 12 Oct 2026 · 09:00–16:00
Instructors: Aya Alsaqaf, Ali Taqi

An investment-themed, two-day Copilot workshop. It follows the Outlook → Excel → Word/PowerPoint → Outlook workflow. Every exercise uses fictional client portfolios: Al-Murjan for trainees, and Al-Waha for the instructor demos.

## Folders

| Folder | What it is | Deploy? |
|---|---|---|
| `site/` | The public site: landing page, day pages, decks, trainee labs, case files, practice files, cheat sheet | **Yes — this is the web root** |
| `facilitator/` | The full kit: everything in `site/` plus presenter notes, answer keys, walkthroughs, instructor labs and solutions, run-of-show, project scoring guide and sheet | **No — keep private (contains flags and answers)** |
| `build/` | Generator source that produces both folders | No |

## Start here

- **Public site:** `site/index.html`
- **Facilitator index:** `facilitator/workshop-index.html`
- **Run-of-show:** `facilitator/run-of-show.html`
- **Scoring:** `facilitator/project-and-scoring.html` and `kamco-p2-scoring-sheet.xlsx` (35 trainees, ranked to approve 30 for Program 3)

## Rebuild

```bash
cd build
npm install
bash build_all.sh                    # writes build/out/site, out/facilitator, out/all
cp out/site/* ../site/ && cp out/all/* ../facilitator/
node validate.js                     # optional: Playwright checks (set CHR=/path/to/chromium)
```

- **Content:** edit `content_day1.py`, `content_day2.py` (decks) and `lab_content.py` (labs, including "Finished early?" extras).
- **Scenario numbers:** defined in `scenarios.py`; answers are written to `out/answers.json`.
- **Templates:** `build/templates/` holds the CODED workshop-builder base templates. Override the path with `WB_EXAMPLES`.

## Before the workshop

- **MAP test QR codes:** paste the pre and post MAP test links into `deckkit2.install({"pre": "…", "post": "…"})` in `build/build_decks.py`, then rebuild. Until then, the QR slides show a placeholder.
