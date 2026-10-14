import bisect
from collections import defaultdict
from collections import deque
from functools import lru_cache
import heapq
from locale import resetlocale
from pickle import FALSE
import random
import math
from collections import Counter
import sys
 
#parse a single integer
mod = 10**9+7
def inp():
    return(int(sys.stdin.readline()))
#parse a list of integers
def inlt():
    return(list(map(int,sys.stdin.readline().split())))
#parse a string (can be modified to parse a list of characters)
def insr():
    s = sys.stdin.readline()[:-1]
    return(s)
#no idea what this does
def invr():
    return(map(int,input().split()))
def gcd(a,b):
    if b == 0:
        return a
    return gcd(b, a % b)
class UF:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [0] * size
        
    def find(self, x):
        if self.parent[x] == x:
            return x
        return self.find(self.parent[x])
    
    def union(self, x, y):
        px = self.find(x)
        py = self.find(y)
        if px == py:
            return
        if self.rank[px] > self.rank[py]:
            self.parent[py] = px
        elif self.rank[px] < self.rank[py]:
            self.parent[px] = py
        else:
            self.parent[px] = py
            self.rank[py] += 1

class BIT:
    def __init__(self, n):
        self.sums = [0] * (n+1)
    
    def update(self, i, delta):
        while i < len(self.sums):
            self.sums[i] += delta
            i += i & (-i)
    
    def query(self, i):
        res = 0
        while i > 0:
            res += self.sums[i]
            i -= i & (-i)
        return res

class NumArray:
    def __init__(self, nums):
        self.bit = BIT(len(nums))
        for i, num in enumerate(nums):
            self.bit.update(i+1, num)
        self.nums = [0] + nums

    def update(self, i, val):
        self.bit.update(i+1, val - self.nums[i+1])
        self.nums[i+1] = val

    def sumRange(self, i, j):
        return self.bit.query(j+1) - self.bit.query(i)

# z = inp()
mod = 998244353
for v in range(1):
    n = inp()

    manager = [-1] * n 
    children = defaultdict(list)
    for i in range(n):
        m = inp()
        children[m-1].append(i)
    print(children)
    res = 0
    dp = defaultdict(int)
    def dfs(node):
        if node in dp:
            return dp[node]
        tmp = 0

        for c in children[node]:
            tmp = max(tmp, dfs(c))
        dp[node] = tmp + 1
        return 1 + tmp 
    res = 0
    for i in range(n):
        res = max(res, dfs(i))

    print(res)