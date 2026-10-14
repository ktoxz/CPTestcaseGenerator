from functools import cache
from math import comb

n, m, h = map(int, input().split())
a = list(map(int, input().split()))

if sum(a) < n:
    print(-1)
    exit(0)

a[h - 1] -= 1
n -= 1


@cache
def helper(i, remaining):
    if remaining == 0:
        return 1
    if i < 0:
        return 0
    ans = 0
    for j in range(min(a[i], remaining) + 1):
        ans += comb(a[i], j) * helper(i - 1, remaining - j)
    return ans


@cache
def helper2(i, remaining):
    if remaining == 0:
        return 1
    if i < 0:
        return 0
    ans = 0
    for j in range(min(a[i], remaining) + 1):
        ans += helper2(i - 1, remaining - j)
    return ans


x = helper(m - 1, n)
a = a[:h - 1] + a[h:]
y = helper2(m - 2, n)

print(1 - (y / x))