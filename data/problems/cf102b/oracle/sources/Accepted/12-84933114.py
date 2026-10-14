"""
  ____          _      _____
 / ___|___   __| | ___|  ___|__  _ __ ___ ___  ___
| |   / _ \ / _` |/ _ \ |_ / _ \| '__/ __/ _ \/ __|
| |__| (_) | (_| |  __/  _| (_) | | | (_|  __/\__ \
 \____\___/ \__,_|\___|_|  \___/|_|  \___\___||___/

"""
"""
░░██▄░░░░░░░░░░░▄██
░▄▀░█▄░░░░░░░░▄█░░█░
░█░▄░█▄░░░░░░▄█░▄░█░
░█░██████████████▄█░
░█████▀▀████▀▀█████░
▄█▀█▀░░░████░░░▀▀███
██░░▀████▀▀████▀░░██
██░░░░█▀░░░░▀█░░░░██
███▄░░░░░░░░░░░░▄███
░▀███▄░░████░░▄███▀░
░░░▀██▄░▀██▀░▄██▀░░░
░░░░░░▀██████▀░░░░░░
░░░░░░░░░░░░░░░░░░░░
"""

import sys
import math
import collections
import operator as op
from collections import deque
from math import gcd, inf, sqrt
from bisect import bisect_right, bisect_left

#sys.stdin = open('input.txt', 'r')
#sys.stdout = open('output.txt', 'w')

from functools import reduce
from sys import stdin, stdout, setrecursionlimit
setrecursionlimit(2**20)


def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


def ncr(n, r):
    r = min(r, n - r)
    numer = reduce(op.mul, range(n, n - r, -1), 1)
    denom = reduce(op.mul, range(1, r + 1), 1)
    return numer // denom  # or / in Python 2


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return len(set(factors))


def isPowerOfTwo(x):
    return (x and (not(x & (x - 1))))


def factors(n):
    return list(set(reduce(list.__add__, ([i, n // i] for i in range(1, int(n**0.5) + 1) if n % i == 0))))

MOD = 10**9 + 7
T = 1
# T = int(stdin.readline())
for _ in range(T):
    # a, b = list(map(int, stdin.readline().split()))
    # s1 = list(stdin.readline().strip('\n'))
    # s2 = list(stdin.readline().strip('\n'))
    #n = int(stdin.readline())
    # a, b, n = list(map(int, stdin.readline().split()))
    # n, k = list(map(int, stdin.readline().split()))
    n = str(stdin.readline().strip('\n'))
    # s2 = str(stdin.readline().strip('\n'))
    d = {}
    k = 0
    while len(n) > 1:
        ans = 0
        for i in n:
            ans += int(i)
        n = str(ans)
        k += 1
    print(k)