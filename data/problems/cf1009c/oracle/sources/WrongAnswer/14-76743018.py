import os, sys, bisect, copy
from collections import defaultdict, Counter, deque
from functools import lru_cache   #use @lru_cache(None)
if os.path.exists('in.txt'): sys.stdin=open('in.txt','r')
if os.path.exists('out.txt'): sys.stdout=open('out.txt', 'w')
#
def input(): return sys.stdin.readline()
def mapi(arg=0): return map(int if arg==0 else str,input().split())
#------------------------------------------------------------------


n,m = mapi()
res = 0
for i in range(m):
    x,d = mapi()
    res+=x*n
    if d>0:
        res+=d*n*(n-1)/2
    else:
        if n&1:
            res+=2*d*(n/2+1)*(n/2)/2
        else:
            res+=2*d*(n/2-1)*(n/2)/2
            res+=(n/2)*d
print("{:.10f}".format(res/n))