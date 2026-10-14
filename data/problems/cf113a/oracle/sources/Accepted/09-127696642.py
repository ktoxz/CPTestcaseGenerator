import sys
from functools import lru_cache, cmp_to_key
from heapq import merge, heapify, heappop, heappush
from math import *
from collections import defaultdict as dd, deque, Counter as C
from itertools import combinations as comb, permutations as perm
from bisect import bisect_left as bl, bisect_right as br, bisect, insort
from time import perf_counter
from fractions import Fraction
import copy
from copy import deepcopy
import time
starttime = time.time()
mod = int(pow(10, 9) + 7)
mod2 = 998244353

def data(): return sys.stdin.readline().strip()
def out(*var, end="\n"): sys.stdout.write(' '.join(map(str, var))+end)
def L(): return list(sp())
def sl(): return list(ssp())
def sp(): return map(int, data().split())
def ssp(): return map(str, data().split())
def l1d(n, val=0): return [val for i in range(n)]
def l2d(n, m, val=0): return [l1d(n, val) for j in range(m)]
try:
    # sys.setrecursionlimit(int(pow(10,6)))
    sys.stdin = open("input.txt", "r")
    sys.stdout = open("../output.txt", "w")
except:
    pass
def pmat(A):
    for ele in A: print(*ele,end="\n")

# from sys import stdin
# input = stdin.buffer.readline
# I = lambda : list(map(int,input().split()))

# import sys
# input=sys.stdin.readline





def f(a):
    b=len(a)
    if b>=4 and a[-4:]=='lios':
        return [1,1]
    if b>=5 and a[-5:]=='liala':
        return [1,2]
    if b>=3 and a[-3:]=='etr':
        return [2,1]
    if b>=4 and a[-4:]=='etra':
        return [2,2]
    if b>=6 and a[-6:]=='initis':
        return [3,1]
    if b>=6 and a[-6:]=='inites':
        return [3,2]
    return -1
a=[f(i) for i in input().split()]
n=len(a)
if -1 in a or [i[1] for i in a]!=[a[0][1]]*n:
    print('NO')
else:
    i,j=0,n-1
    while i<n and a[i][0]==1:
        i+=1
    while j>=0 and a[j][0]==3:
        j-=1
    print('YES' if i==j or n==1 else 'NO')