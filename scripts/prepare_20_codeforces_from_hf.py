import os
import sys
import time
import json
import re
import html
import hashlib
from pathlib import Path
import urllib.request
import pyarrow.parquet as pq

# Add repo root to sys.path
ROOT = Path("d:/KLTN/Final_TestcaseGenerator")
sys.path.insert(0, str(ROOT))
from testgen.codenet import find_local_oracle_bundle, LocalCodeNetSource
from testgen.pipeline import samples

PARQUET_FILE = ROOT / "data" / "cache_hf" / "0000.parquet"
PROBLEMS_DIR = ROOT / "data" / "problems"

PROBLEMS_TO_EXTRACT = [
    ("1008", "A"),
    ("1009", "A"),
    ("1011", "A"),
    ("1006", "A"),
    ("1003", "A"),
    ("1004", "A"),
    ("1007", "A"),
    ("1008", "B"),
    ("1005", "A"),
    ("1005", "B"),
    ("1011", "B"),
    ("1000", "A"),
    ("1006", "C"),
    ("1009", "B"),
    ("1006", "B"),
    ("1004", "B"),
    ("1004", "C"),
    ("1000", "B"),
    ("1003", "C"),
    ("1003", "B"),
]

def fetch_and_format_cf_statement(contest_id: str, problem_index: str):
    url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw_html = resp.read().decode('utf-8', errors='replace')
            break
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(2)

    # Title
    t_match = re.search(r'<div class="title">\s*([^<]+)\s*</div>', raw_html)
    title = html.unescape(t_match.group(1).strip()) if t_match else f"{problem_index}. Problem {contest_id}{problem_index}"

    # Time limit
    tl_match = re.search(r'<div class="time-limit"[^>]*>.*?</div>\s*([\d.]+)\s*seconds?', raw_html, re.DOTALL)
    tl_sec = float(tl_match.group(1)) if tl_match else 1.0
    time_limit_str = f"{int(tl_sec) if tl_sec.is_integer() else tl_sec} second{'s' if tl_sec > 1 else ''}"

    # Memory limit
    ml_match = re.search(r'<div class="memory-limit"[^>]*>.*?</div>\s*(\d+)\s*megabytes', raw_html, re.DOTALL)
    ml_mb = int(ml_match.group(1)) if ml_match else 256
    memory_limit_str = f"{ml_mb} megabytes"

    # Find problem statement container
    start = raw_html.find('<div class="problem-statement">')
    if start == -1:
        raise ValueError(f"problem-statement not found for {contest_id}/{problem_index}")
    end = raw_html.find('<script type="text/javascript">', start)
    if end == -1:
        end = start + 35000
    stmt_html = raw_html[start:end]

    # Description
    desc_start = stmt_html.find('</div></div><div>')
    if desc_start == -1:
        desc_start = stmt_html.find('</div>\n</div>\n<div>')
    if desc_start == -1:
        desc_start = stmt_html.find('</div>', stmt_html.find('<div class="output-file"')) + 6
    desc_end = stmt_html.find('<div class="input-specification">')
    desc_raw = stmt_html[desc_start:desc_end] if desc_end != -1 else ""

    def clean_html(h):
        h = html.unescape(h)
        h = re.sub(r'<div[^>]*>', '\n', h)
        h = re.sub(r'<p[^>]*>', '\n', h)
        h = re.sub(r'</p>', '\n', h)
        h = re.sub(r'<br\s*/?>', '\n', h)
        h = re.sub(r'<[^>]+>', '', h)
        lines = [line.strip() for line in h.splitlines()]
        return '\n'.join([l for l in lines if l])

    desc_text = clean_html(desc_raw)

    # Input specification
    inp_spec_match = re.search(r'<div class="input-specification">(.*?)</div>\s*<div class="output-specification">', stmt_html, re.DOTALL)
    inp_text = clean_html(inp_spec_match.group(1)) if inp_spec_match else ""
    if inp_text.startswith("Input"):
        inp_text = inp_text[5:].strip()

    # Output specification
    out_spec_match = re.search(r'<div class="output-specification">(.*?)</div>\s*<div class="sample-tests">', stmt_html, re.DOTALL)
    out_text = clean_html(out_spec_match.group(1)) if out_spec_match else ""
    if out_text.startswith("Output"):
        out_text = out_text[6:].strip()

    # Note
    note_match = re.search(r'<div class="note">(.*?)</div>', stmt_html, re.DOTALL)
    note_text = clean_html(note_match.group(1)) if note_match else ""
    if note_text.startswith("Note"):
        note_text = note_text[4:].strip()

    # Samples
    inputs_raw = re.findall(r'<div class="input"[^>]*>.*?<pre[^>]*>(.*?)</pre>', stmt_html, re.DOTALL)
    outputs_raw = re.findall(r'<div class="output"[^>]*>.*?<pre[^>]*>(.*?)</pre>', stmt_html, re.DOTALL)
    def clean_pre(raw):
        text = re.sub(r'<br\s*/?>', '\n', raw, flags=re.IGNORECASE)
        text = re.sub(r'</?div[^>]*>', '\n', text)
        text = html.unescape(text)
        text = re.sub(r'<[^>]+>', '', text)
        lines = [line.rstrip() for line in text.splitlines()]
        return '\n'.join(lines).strip() + '\n'

    sample_pairs = []
    for in_r, out_r in zip(inputs_raw, outputs_raw):
        s_in = clean_pre(in_r)
        s_out = clean_pre(out_r)
        sample_pairs.append((s_in, s_out))

    # Build Markdown
    md_parts = [
        f"# {title}\n",
        f"Source: {url}\n",
        f"{title}",
        "time limit per test",
        time_limit_str,
        "memory limit per test",
        memory_limit_str,
        "input",
        "standard input",
        "output",
        "standard output\n",
        desc_text + "\n",
        "Input",
        inp_text + "\n",
        "Output",
        out_text + "\n",
        "## Examples\n"
    ]

    for s_idx, (s_in, s_out) in enumerate(sample_pairs, 1):
        md_parts.append(f"## Sample Input {s_idx}\n```text\n{s_in}```\n")
        md_parts.append(f"## Output for the Sample Input {s_idx}\n```text\n{s_out}```\n")

    if note_text:
        md_parts.append("Note\n" + note_text + "\n")

    markdown = '\n'.join(md_parts)
    metadata = {
        "problem_id": f"cf{contest_id}{problem_index.lower()}",
        "contest_id": int(contest_id),
        "index": problem_index,
        "title": title,
        "url": url,
        "time_limit_ms": int(tl_sec * 1000),
        "memory_limit_mb": ml_mb,
        "samples": [{"input": si, "output": so} for si, so in sample_pairs]
    }
    return markdown, metadata, sample_pairs

def main():
    print(f"Reading {PARQUET_FILE}...")
    table = pq.read_table(
        PARQUET_FILE,
        columns=['problem_id', 'contestId', 'problem_index', 'verdict', 'programmingLanguage', 'source']
    )
    df = table.to_pandas()
    print(f"Total rows in parquet: {len(df)}")

    def get_lang_dialect_ext(prog_lang: str):
        if 'Python 3' in prog_lang or 'PyPy 3' in prog_lang:
            return 'Python', 'Python3', '.py'
        elif 'C++' in prog_lang:
            return 'C++', 'C++17', '.cpp'
        elif 'GNU C' in prog_lang:
            return 'C', 'C', '.c'
        return None, None, None

    created_problems = []

    for idx, (cid, pidx) in enumerate(PROBLEMS_TO_EXTRACT, 1):
        pid = f"{cid}/{pidx}"
        slug = f"cf{cid}{pidx.lower()}"
        pdir = PROBLEMS_DIR / slug
        print(f"\n[{idx}/20] Processing {slug} ({pid})...")

        # 1. Fetch statement & metadata
        try:
            statement_md, metadata, sample_pairs = fetch_and_format_cf_statement(cid, pidx)
        except Exception as e:
            print(f"  Error fetching statement for {pid}: {e}")
            continue

        pdir.mkdir(parents=True, exist_ok=True)
        (pdir / "statement.md").write_text(statement_md, encoding="utf-8")
        (pdir / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        (pdir / "checker.json").write_text(json.dumps({"kind": "TOKEN"}, indent=2) + "\n", encoding="utf-8")

        # 2. Extract Oracle submissions
        prob_subs = df[df['problem_id'] == pid]
        
        # Valid languages
        valid_rows = []
        for _, row in prob_subs.iterrows():
            lang, dialect, ext = get_lang_dialect_ext(str(row['programmingLanguage']))
            if lang:
                valid_rows.append((row, lang, dialect, ext))
        
        ac_candidates = [item for item in valid_rows if item[0]['verdict'] == 'OK'][:10]
        wa_candidates = [item for item in valid_rows if item[0]['verdict'] == 'WRONG_ANSWER'][:10]

        oracle_dir = pdir / "oracle"
        sources_ac = oracle_dir / "sources" / "Accepted"
        sources_wa = oracle_dir / "sources" / "WrongAnswer"
        sources_ac.mkdir(parents=True, exist_ok=True)
        sources_wa.mkdir(parents=True, exist_ok=True)

        # Clear any existing old files in sources
        for f in sources_ac.glob("*"): f.unlink()
        for f in sources_wa.glob("*"): f.unlink()

        manifest = []

        # Save AC
        for ac_idx, (row, lang, dialect, ext) in enumerate(ac_candidates, 1):
            src_file = sources_ac / f"{ac_idx}{ext}"
            src_file.write_text(str(row['source']), encoding="utf-8", errors="replace")
            manifest.append({
                "id": f"{slug}-ac-{ac_idx}",
                "problem_id": slug,
                "label": "Accepted",
                "language": lang,
                "dialect": dialect,
                "source": f"sources/Accepted/{ac_idx}{ext}",
                "sha256": hashlib.sha256(src_file.read_bytes()).hexdigest(),
            })

        # Save WA
        for wa_idx, (row, lang, dialect, ext) in enumerate(wa_candidates, 1):
            src_file = sources_wa / f"{wa_idx}{ext}"
            src_file.write_text(str(row['source']), encoding="utf-8", errors="replace")
            manifest.append({
                "id": f"{slug}-wa-{wa_idx}",
                "problem_id": slug,
                "label": "Wrong Answer",
                "language": lang,
                "dialect": dialect,
                "source": f"sources/WrongAnswer/{wa_idx}{ext}",
                "sha256": hashlib.sha256(src_file.read_bytes()).hexdigest(),
            })

        (oracle_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        # 3. Validation
        parsed_samples = samples(statement_md)
        bundle = find_local_oracle_bundle(PROBLEMS_DIR, slug)
        assert bundle is not None, f"Local oracle bundle not found for {slug}"
        assert len(parsed_samples) > 0, f"No samples parsed for {slug}"
        assert len(ac_candidates) >= 5, f"Not enough AC candidates for {slug}: {len(ac_candidates)}"
        assert len(wa_candidates) >= 5, f"Not enough WA candidates for {slug}: {len(wa_candidates)}"

        print(f"  Title: {metadata['title']}")
        print(f"  Samples: {len(parsed_samples)}, Oracle: {len(ac_candidates)} AC + {len(wa_candidates)} WA")
        created_problems.append(slug)
        time.sleep(0.3)


    print("\n" + "="*60)
    print(f"Successfully prepared {len(created_problems)}/20 problems!")
    print("Created problem list:")
    print(" ".join(created_problems))
    print("="*60)

if __name__ == "__main__":
    main()
