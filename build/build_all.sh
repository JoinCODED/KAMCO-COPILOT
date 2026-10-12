set -e
cd "$(dirname "$0")"
[ -d node_modules/qrcode-generator ] || npm install --silent
rm -rf out/site out/facilitator out/all
mkdir -p out/site out/facilitator
python3 gen_files.py >/dev/null && python3 gen_docs.py >/dev/null && python3 gen_promptlib.py >/dev/null && python3 gen_capstone.py >/dev/null && python3 gen_agentdocs.py >/dev/null
python3 build_decks.py
python3 build_labs.py
python3 tasklab_day1.py
python3 tasklab_day2.py
python3 build_pages.py >/dev/null
python3 deck2_mcim.py
python3 build_facil.py >/dev/null
python3 build_capstone_key.py
python3 gen_instructor_agent.py
python3 build_index.py
RECALC="${RECALC:-/mnt/skills/public/xlsx/scripts/recalc.py}"
[ -f "$RECALC" ] && python3 "$RECALC" out/facilitator/kamco-p2-scoring-sheet.xlsx 60 | grep status || echo "recalc skipped (open the xlsx in Excel to compute formulas)"
python3 rebrand.py
mkdir -p out/all && cp out/site/* out/all/ && cp out/facilitator/* out/all/ && cp manifest.json out/all/
