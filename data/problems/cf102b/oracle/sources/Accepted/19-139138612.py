import sys
import pprint
import logging
from logging import getLogger

def input(): return sys.stdin.readline().rstrip("\r\n")


logging.basicConfig(format="%(message)s", level=logging.WARNING,)
logger = getLogger(__name__)
logger.setLevel(logging.INFO)


def debug(msg, *args):
    logger.info(f'{msg}={pprint.pformat(args)}')

# 30 MINUTES ATLEAST !!!!

###################################################################################################################

# let's do this by recursion


def printPattern(t, n):
    if t == n + 1:
        return

    for i in range(n - t):
        print(' ', end=' ')

    for i in range(t + 1):
        print(i, end=' ')

    for i in range(t - 1, 0, -1):
        print(i, end=' ')

    print(0)

    printPattern(t + 1, n)

    if t == n:
        return
    for i in range(n - t):
        print(' ', end=' ')

    for i in range(t + 1):
        print(i, end=' ')

    for i in range(t - 1, 0, -1):
        print(i, end=' ')

    print(0)


def single():
    return map(int, input().split())

# interior angle of a polygon is defined as angle b/w any two adjacent sides, i.e  180 * (n - 2) // n
# DON'T LOOK AT TEST CASES !!


def t():
    s = [int(i) for i in input()]
    ans = 0
    while len(s) > 1:
        summ = sum(s)
        s = [int(i) for i in str(summ)]
        ans += 1
    print(ans)


t()