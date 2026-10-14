import sys
input = lambda: sys.stdin.readline().rstrip()
import math
import random
from bisect import bisect_right, bisect_left
from itertools import product, permutations, combinations, combinations_with_replacement 
from collections import deque, defaultdict, Counter
from heapq import heapify, heappush, heappop
from functools import lru_cache, reduce
inf = float('inf')
def error(*args, sep=' ', end='\n'):
  print(*args, sep=sep, end=end, file=sys.stderr)
# mod = 1000000007
# mod = 998244353
DIR = [(0, 1), (0, -1), (1, 0), (-1, 0)]

#  -----------------------  #

n = int(input())
s = input()
t = input()
ans = 0
for i in range(n//2):
  a = s[i]
  b = s[n-i-1]
  c = t[i]
  d = t[n-i-1]
  if c == d:
    if a != b:
      if a == c:
        ans += 1
      elif b == c:
        ans += 1
  else:
    if a == b:
      if a == c:
        ans += 1
      elif a == d:
        ans += 1
      else:
        ans += 2
    else:
      if (a == c or a == d) and (b == c or b == d):
        pass
      elif a == c or a == d:
        ans += 1
      elif b == c or b == d:
        ans += 1
      else:
        ans += 1
if n & 1:
  a = s[n//2]
  b = t[n//2]
  ans += a != b
print(ans)