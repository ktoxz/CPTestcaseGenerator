from collections import defaultdict
import sys
import math
s = input()
n = len(s)
k = int(input())
m = {}
for c in s:
    m[c] = m.get(c, 0) + 1
m = dict(sorted(m.items(), key=lambda x: x[1]))
for c, v in m.items():
    if v < k:
        s = s.replace(c, '')
    else:
        break
    k -= v
print(len(set(s)))
print(s)