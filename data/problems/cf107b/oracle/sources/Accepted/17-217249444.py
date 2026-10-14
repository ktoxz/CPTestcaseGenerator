import math

n,m,h = map(int,input().split())
s = list(map(int,input().split()))

if sum(s) < n:
    print(-1)
else:
    A = math.comb(sum(s) - s[h - 1], n - 1)
    B = math.comb(sum(s) - 1, n - 1)
    print(1 - A/B)# 1691237684.1318727