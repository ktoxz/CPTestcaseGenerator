import urllib.request
import re
import html

def clean_pre(raw):
    text = re.sub(r'<br\s*/?>', '\n', raw, flags=re.IGNORECASE)
    text = re.sub(r'</?div[^>]*>', '\n', text)
    text = html.unescape(text)
    text = re.sub(r'<[^>]+>', '', text)
    lines = [line.rstrip() for line in text.splitlines()]
    return '\n'.join(lines).strip() + '\n'

url = 'https://codeforces.com/contest/1003/problem/A'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
raw = urllib.request.urlopen(req).read().decode('utf-8')
inps = re.findall(r'<div class="input"[^>]*>.*?<pre[^>]*>(.*?)</pre>', raw, re.DOTALL)
outs = re.findall(r'<div class="output"[^>]*>.*?<pre[^>]*>(.*?)</pre>', raw, re.DOTALL)

for i, (inp, out) in enumerate(zip(inps, outs), 1):
    print(f'=== Sample {i} Input ===')
    print(clean_pre(inp))
    print(f'=== Sample {i} Output ===')
    print(clean_pre(out))
