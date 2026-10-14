import time
import sys
import math
def get_primes(n):
    sieve = [True] * n
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3,n,2) if sieve[i]]
from bisect import bisect, bisect_left, bisect_right, insort, insort_left, insort_right
from functools import reduce
def factors(n):
    return set(reduce(list.__add__,([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
input = sys.stdin.readline
mod, infi = 1000000007, sys.maxsize
from collections import deque, Counter, defaultdict as dd
from heapq import heappop, heappush, heapify
from itertools import accumulate
from functools import lru_cache, reduce
from operator import mul, add, sub, truediv, floordiv, lt, le, eq, ne, gt, xor, concat, getitem, lshift
inty    =lambda: int(input())
stringy =lambda: input().strip()
normal  =lambda: input().split()
mappy   =lambda: map(int,input().strip().split())
fmappy  =lambda: map(float,input().strip().split())
listy   =lambda: list(map(int,input().strip().split()))
#sys.setrecursionlimit(10**6)
tick    =lambda: time.perf_counter()
logg    =lambda a, b: math.log2(a) / math.log2(b)
acc     =lambda x: list(accumulate(x))
sign    =lambda x, y: x >= 0 and y >= 0 or x < 0 and y < 0

n = inty()
chosen = []
possi = []
delete = []
for i in range(n):
    s, r, h, c = mappy()
    possi.append((s, r, h, c, i + 1))
for i, p in enumerate(possi):
    s, r, h, c, k = p
    for j in range(n):
        if j == i: continue
        s1, r1, h1, c1, kk = possi[j]
        if s < s1 and r < r1 and h < h1:
            delete.append(p)
            break
for p in delete:
    possi.remove(p)
possi.sort(key = lambda x: x[3])
print(possi[0][4])