import urllib.request
import re
import html
from html.parser import HTMLParser

url = 'https://codeforces.com/contest/1008/problem/A'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
with urllib.request.urlopen(req, timeout=15) as resp:
    raw = resp.read().decode('utf-8')

m = re.search(r'<div class="title">\s*([^<]+)\s*</div>', raw)
print('Title:', m.group(1) if m else 'None')

inputs = re.findall(r'<div class="input"[^>]*>.*?<pre[^>]*>(.*?)</pre>', raw, re.DOTALL)
outputs = re.findall(r'<div class="output"[^>]*>.*?<pre[^>]*>(.*?)</pre>', raw, re.DOTALL)
print('Inputs found:', len(inputs))
print('Outputs found:', len(outputs))
if inputs and outputs:
    clean_in = html.unescape(re.sub(r'<div[^>]*>', '\n', inputs[0]))
    clean_in = re.sub(r'<[^>]+>', '', clean_in).strip()
    clean_out = html.unescape(re.sub(r'<div[^>]*>', '\n', outputs[0]))
    clean_out = re.sub(r'<[^>]+>', '', clean_out).strip()
    print('Sample 1 in:\n' + repr(clean_in))
    print('Sample 1 out:\n' + repr(clean_out))
