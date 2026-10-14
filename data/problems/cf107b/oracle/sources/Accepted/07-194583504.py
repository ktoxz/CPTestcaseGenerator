# Thank God that I'm not you.
from itertools import permutations, combinations;
import heapq;
from collections import Counter, deque;
import math;
import sys;
from functools import lru_cache;


input = sys.stdin.readline;

n, m, k = map(int, input().split())

array = list(map(int, input().split()))

def solve():
    if sum(array) < n:
        return -1;

    array[k - 1] -= 1;

    if not array[k - 1]:
        return 0;

    p = 1;
    currSum = sum(array) - array[k - 1];
    totalSum = sum(array)
    for i in range(1, n):
        p *= (currSum / totalSum)
        currSum -= 1;
        totalSum -= 1;

    return 1 - p;




print(solve())