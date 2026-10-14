import sys
import math
import copy
from collections import deque
from collections import *
from functools import lru_cache
import cmath

input = lambda: sys.stdin.readline().rstrip("\r\n")


# sys.stdin = open('input.txt')
# sys.stdout = open('output.txt', 'w')

def ll(): return list(map(int, input().split()))


def lf(): return list(map(float, input().split()))


def ls(): return list(map(str, input().split()))


def mn(): return map(int, input().split())


def nt(): return int(input())


def ns(): return input()
def fc(n):
    ans = Counter()
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans[d]+=1
            n //= d
        else:
            d += 1
    if n > 1:
        ans[n]+=1
    return ans

def ip(n):
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n and n % d != 0:
        d += 2
    return d * d > n


@lru_cache(None)
def daa(n):
    ct = 0
    for x in range(1, int(pow(n, 0.5)) + 1):
        if n % x == 0:
            ct += 1
            if x != n // x:
                ct += 1
    return ct
n=nt()
k=nt()
p=fc(k)
h=fc(n)
ans=set()
for x in p:
    if h[x]>0:
        if p[x]%h[x]==0:
            ans.add(p[x]//h[x])
            continue
        else:
            print("NO")
            exit(0)
    else:
        print("NO")
        exit(0)
if len(ans)>1:
    print("NO")
else:
    print("YES")
    for x in ans:
        k=x
    print(k-1)