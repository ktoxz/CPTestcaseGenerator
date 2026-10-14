# Thank God that I'm not you.
from itertools import permutations, combinations;
import heapq;
from collections import Counter, deque;
import math;
import sys;
from functools import lru_cache;

def nCR(n, r):
    # p holds the value of n*(n-1)*(n-2)...,
    # k holds the value of r*(r-1)...
    p = 1
    k = 1

    # C(n, r) == C(n, n-r),
    # choosing the smaller value
    if (n - r < r):
        r = n - r

    if (r > 0):
        while (r):
            p *= n
            k *= r

            # gcd of p, k
            m = math.gcd(p, k)

            # dividing by gcd, to simplify product
            # division by their gcd saves from
            # the overflow
            p //= m
            k //= m

            n -= 1
            r -= 1

    else:
        p = 1

    return p;


n, m, k = map(int, input().split())

array = list(map(int, input().split()))

def solve():
    if sum(array) < n:
        return -1;

    array[k - 1] -= 1;

    if not array[k - 1]:
        return 0;

    currN = array[k - 1]
    currSum = 0;

    totalSum = sum(array)
    for i in range(1, n):
        currSum += (nCR(currN, i) * nCR(totalSum - currN, (n - 1) - i))
    return currSum / (nCR(sum(array), n - 1));

print(solve())