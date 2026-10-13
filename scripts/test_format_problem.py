import urllib.request
import re
import html
from html.parser import HTMLParser
import sys
sys.path.insert(0, 'd:/KLTN/Final_TestcaseGenerator')
from testgen.pipeline import samples

def fetch_and_format_cf_problem(contest_id: str, problem_index: str):
    url = f"https://codeforces.com/contest/{contest_id}/problem/{problem_index}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw_html = resp.read().decode('utf-8')

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

    # Find problem statement div
    start = raw_html.find('<div class="problem-statement">')
    if start == -1:
        raise ValueError(f"problem-statement not found for {contest_id}/{problem_index}")
    end = raw_html.find('<script type="text/javascript">', start)
    if end == -1:
        end = start + 30000
    stmt_html = raw_html[start:end]

    # Description (between header div and input-specification)
    desc_start = stmt_html.find('</div></div><div>')
    if desc_start == -1:
        desc_start = stmt_html.find('</div>\n</div>\n<div>')
    if desc_start == -1:
        desc_start = stmt_html.find('</div>', stmt_html.find('<div class="output-file"')) + 6
    desc_end = stmt_html.find('<div class="input-specification">')
    desc_raw = stmt_html[desc_start:desc_end] if desc_end != -1 else ""

    # Clean text helper
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
    sample_pairs = []
    for in_r, out_r in zip(inputs_raw, outputs_raw):
        s_in = html.unescape(re.sub(r'<div[^>]*>', '\n', in_r))
        s_in = re.sub(r'<[^>]+>', '', s_in).strip() + "\n"
        s_out = html.unescape(re.sub(r'<div[^>]*>', '\n', out_r))
        s_out = re.sub(r'<[^>]+>', '', s_out).strip() + "\n"
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

md, meta, sp = fetch_and_format_cf_problem("1008", "A")
print("Parsed title:", meta["title"])
print("Samples count:", len(sp))
parsed_samples = samples(md)
print("Pipeline samples count:", len(parsed_samples))
assert len(parsed_samples) == len(sp), "Pipeline samples must match extracted samples"
print("Verification passed!")
