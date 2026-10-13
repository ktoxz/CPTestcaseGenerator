import sys
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from testgen.pipeline import samples
from scripts.prepare_20_codeforces_from_hf import PROBLEMS_TO_EXTRACT, PROBLEMS_DIR, fetch_and_format_cf_statement

print("Updating statement.md for all 20 problems...")
for cid, idx in PROBLEMS_TO_EXTRACT:
    slug = f"cf{cid}{idx.lower()}"
    pdir = PROBLEMS_DIR / slug
    if not pdir.is_dir():
        continue
    
    print(f"Fetching {slug} ({cid}/{idx})...")
    md, meta, sp = fetch_and_format_cf_statement(cid, idx)
    (pdir / "statement.md").write_text(md, encoding="utf-8")
    (pdir / "metadata.json").write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    parsed_samples = samples(md)
    print(f"  Done: {len(parsed_samples)} samples parsed cleanly.")

print("All 20 problem statements updated successfully!")
