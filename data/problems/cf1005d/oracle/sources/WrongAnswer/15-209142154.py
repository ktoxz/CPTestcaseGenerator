import sys
input = lambda: sys.stdin.readline().rstrip()
from collections import deque,defaultdict,Counter
from itertools import permutations,combinations
from bisect import *
from heapq import *
from math import ceil,gcd,lcm,floor

S = []
for i in input():
    S.append(int(i)%3)

l = []
num = 0
ans = 0
for i in S:
    l.append(i)
    num+=1
    if l[-1]==0:
        l = [];num = 0;ans+=1

    if num>=2 and l[-1]+l[-2]==3:
        l = [];num = 0;ans+=1

    if num>=3 and l[-1]==l[-2]==l[-3]==1:
        l = [];num = 0;ans+=1

print(ans)