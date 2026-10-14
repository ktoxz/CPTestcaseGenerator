import math
import sys
from bisect import bisect_right, bisect_left, insort_right
from collections import Counter, defaultdict
from heapq import heappop, heappush
from itertools import accumulate, permutations, combinations
from sys import stdout

R = lambda: map(int, input().split())
n, k = R()
xc = yc = (k + 1) // 2
row = [0] + list(accumulate(abs(j - yc) for j in range(1, k + 1)))
dp = [[k + 1 - j for j in range(k + 1)] for _ in range(k + 1)]
for l in R():
    xt, yt, c = -1, -1, math.inf
    for i in range(1, k + 1):
        for j in range(1, k + 1 - l + 1):
            if dp[i][j] >= l:
                ct = row[j + l - 1] - row[j - 1] + abs(i - xc) * l
                if ct < c or (ct == c and i < xt) or (ct == c and i == xt and j < yt):
                    xt, yt, c = i, j, ct
    if c < math.inf:
        for j in range(yt + l - 1, 0, -1):
            dp[xt][j] = max(0, yt - j)
        print(xt, yt, yt + l - 1, sep=' ')
    else:
        print(-1)