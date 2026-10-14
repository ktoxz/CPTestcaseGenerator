import sys
import math

n, m, k = (sys.stdin.readline()).split()
n = int(n)
m = int(m)
k = float(k)

d = dict()
c = 0
for i in range(n):
    name, exp = (sys.stdin.readline()).split()
    if name not in d:
        v = int(int(exp) * k)
        if(v >= 100):
            c += 1
            d[name] = v
        
for i in range(m):
    name = (sys.stdin.readline()).split()[0]
    if name not in d:
        c += 1
        d[name] = 0
        
print(c)
lk = list(d.keys())
lk.sort()
for i in lk:
    print(str(i) + " " + str(d[i]))