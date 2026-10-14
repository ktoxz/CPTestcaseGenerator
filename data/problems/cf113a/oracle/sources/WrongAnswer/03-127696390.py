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





s=input().split()
x=[]
y=[]
enc=0
gender=-1
for i in range(len(s)):
    if s[i].endswith("etr"):
        if enc:
            print("NO")
            exit()
        if gender==0:
            print("NO")
            exit()
        gender=1
        enc=1
        continue
    elif s[i].endswith("etra"):
        if enc:
            print("NO")
            exit()
        if gender==1:
            print("NO")
            exit()
        gender=0
        enc=1
        continue
    if enc:
        if (s[i].endswith("initis") and gender==0) or  (s[i].endswith("inites") and gender==1) or (not s[i].endswith("initis") and not s[i].endswith("inites")):
            print("NO")
            exit() 
        y.append(s[i])
    else:
        x.append(s[i])
        if x[-1].endswith("lios"):
            if gender==-1:
                gender=1
            elif gender!=1:
                print("NO")
                exit()

        elif x[-1].endswith("liala"):
            if gender==-1:
                gender=0
            elif gender!=0:
                print("NO")
                exit()
        else:
            print("NO")
            exit()
print("YES")