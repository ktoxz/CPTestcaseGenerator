import math
import sys
import queue
import itertools
from heapq import heappop, heappush
import random


def solve():
    n, m, k = map(float, input().split())
    n, m = int(n), int(m)

    new_build = {}

    for i in range(n):
        name, exp = map(str, input().split())
        exp = int(exp)

        new_exp = (k * exp) // 1
        if new_exp >= 100:
            new_build[name] = int(new_exp)

    for i in range(m):
        name = str(input())
        if name not in new_build:
            new_build[name] = 0

    print(len(new_build.keys()))
    order = sorted(list(new_build.keys()))
    for key in order:
        print(key, new_build[key])


if __name__ == '__main__':
    multi_test = 0

    if multi_test:
        t = int(sys.stdin.readline())
        for _ in range(t):
            solve()
    else:
        solve()