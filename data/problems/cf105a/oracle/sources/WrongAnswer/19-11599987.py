import sys
from itertools import *
from math import *
def solve():
    n, m, k = input().split()
    n = int(n)
    m = int(m)
    k = int(k[2:])
    skills = {}
    for i in range(n):
        name, level = input().split()
        level = int(level)
        newlevel = (k * level) // 100
        if newlevel >= 100:
            skills[name] = newlevel
    for i in range(m):
        name = input()
        if name not in skills:
            skills[name] = 0
    print(len(skills))
    for name, val in skills.items():
        print(name, val)


if sys.hexversion == 50594544 : sys.stdin = open("test.txt")
solve()