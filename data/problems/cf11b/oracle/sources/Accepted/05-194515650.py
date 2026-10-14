import sys
input = sys.stdin.readline
from bisect import bisect

c = 0
d = []
for i in range(1, 10**9):
    d.append(c)
    c += i
    if c > 10**9+100000:
        break

x = int(input())
x = abs(x)
a = bisect(d, x)
if d[a-1] == x:
    print(a-1)
else:
    while d[a] % 2 != x%2:
        a += 1
    print(a)