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

rank = {
    '6': 0,
    '7': 1,
    '8': 2,
    '9': 3,
    'T': 4,
    'J': 5,
    'Q': 6,
    'K': 7,
    'A': 8
}
trump = stringy()
f, s = map(str, stringy().split())
print(trump, f[1], s[1])
if (f[-1] == trump and s[-1] != trump) or (f[1] == s[1] and rank[f[0]] > rank[s[0]]): print('YES')
else: print('NO')