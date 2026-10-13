import urllib.request
import re
import html
import json
from pathlib import Path
from html.parser import HTMLParser

url = 'https://codeforces.com/contest/2009/problem/G1'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=20) as resp:
    raw = resp.read().decode('utf-8')

# Find problem statement container
marker = '<div class="problem-statement">'
start = raw.find(marker)
if start == -1:
    print("Could not find problem-statement container!")
    exit(1)

# Find end of problem statement
end = raw.find('<script type="text/javascript">', start)
if end == -1:
    end = start + 30000

stmt_html = raw[start:end]

# Extract title
title_match = re.search(r'<div class="title">\s*([^<]+)\s*</div>', stmt_html)
title = title_match.group(1).strip() if title_match else "G1. Yunli's Subarray Queries (easy version)"

# Extract time limit
tl_match = re.search(r'<div class="time-limit"[^>]*>.*?</div>\s*([\d.]+)\s*seconds?', stmt_html, re.DOTALL)
time_limit = tl_match.group(1).strip() + " seconds" if tl_match else "3 seconds"

# Extract memory limit
ml_match = re.search(r'<div class="memory-limit"[^>]*>.*?</div>\s*(\d+)\s*megabytes', stmt_html, re.DOTALL)
memory_limit = ml_match.group(1).strip() + " megabytes" if ml_match else "256 megabytes"

# Convert mathjax / MathJax spans to dollar signs
# Codeforces uses $$$...$$$ in html or MathJax
stmt_cleaned = re.sub(r'<span class="tex-span">(.*?)</span>', r'$$$\1$$$', stmt_html)

class CleanParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.in_script = False
        self.in_pre = False

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'div', 'tr'):
            self.parts.append('\n')
        elif tag == 'br':
            self.parts.append('\n')
        elif tag == 'pre':
            self.parts.append('\n```\n')
            self.in_pre = True
        elif tag in ('script', 'style'):
            self.in_script = True

    def handle_endtag(self, tag):
        if tag in ('p', 'div', 'tr'):
            self.parts.append('\n')
        elif tag == 'pre':
            self.parts.append('\n```\n')
            self.in_pre = False
        elif tag in ('script', 'style'):
            self.in_script = False

    def handle_data(self, data):
        if not self.in_script:
            self.parts.append(data)

parser = CleanParser()
parser.feed(stmt_cleaned)
extracted_text = ''.join(parser.parts)

# Clean up whitespace
lines = []
for line in extracted_text.splitlines():
    line_s = line.strip()
    if line_s:
        lines.append(line_s)
    elif lines and lines[-1] != "":
        lines.append("")

clean_body = '\n'.join(lines)
output_file = Path("d:/KLTN/Final_TestcaseGenerator/scripts/extracted_g1.txt")
output_file.write_text(clean_body, encoding="utf-8")
print("\nWrote to", output_file)
print("Title:", title)
print("Time limit:", time_limit)
print("Memory limit:", memory_limit)

