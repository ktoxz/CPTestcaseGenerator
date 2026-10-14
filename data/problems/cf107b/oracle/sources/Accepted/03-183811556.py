import sys
input = sys.stdin.readline
from math import comb

n, m, h = map(int, input().split())
w = list(map(int, input().split()))
n -= 1
w[h-1] -= 1
x = sum(w)
if n > x:
    print(-1)
else:
    print((comb(x, n) - comb(x-w[h-1], n))/comb(x, n))