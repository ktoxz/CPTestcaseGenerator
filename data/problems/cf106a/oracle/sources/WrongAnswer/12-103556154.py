def STR(): return list(input())
def INT(): return int(input())
def MAP(): return map(int, input().split())
def MAP2():return map(float,input().split())
def LIST(): return list(map(int, input().split()))
def STRING(): return input()
import string
import sys
from heapq import heappop , heappush
from bisect import *
from collections import deque , Counter
from math import *
from itertools import permutations , accumulate
dx = [-1 , 1 , 0 , 0  ]
dy = [0 , 0  , 1  , - 1]
#visited = [[False for i in range(m)] for j in range(n)]
#sys.stdin = open(r'input.txt' , 'r')
#sys.stdout = open(r'output.txt' , 'w')
#for tt in range(INT()):

s = input()
s1 , s2 = input().split()

l = ["6", "7", "8", "9", "T", "J", "Q", "K" , "A"]
d = {}
for i in range(9):
    d[l[i]] = i

if (s1[1] == s2[1] and d[s1[0]] > d[s2[0]]) or (d[s1[0]] > d[s2[0]] and s1[1] == s):
    print('YES')

else:
    print('NO')