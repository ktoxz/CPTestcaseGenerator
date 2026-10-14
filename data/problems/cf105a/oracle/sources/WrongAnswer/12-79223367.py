#!/usr/bin/env python3

n, m, k = input().rstrip().split()
n, m, k = int(n), int(m), float(k)
cur = {}
for i in range(n):
    skill, exp = input().rstrip().split()
    exp = int(int(exp) * k)
    if exp >= 100:
        cur[skill] = exp

for i in range(m):
    skill = input().rstrip()
    cur.setdefault(skill, 0)

print(len(cur))
for k in sorted(cur.keys()):
    print(k, cur[k])