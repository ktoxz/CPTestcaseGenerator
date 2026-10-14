import time
import math
from sys import stdin, stdout


def I():
    return int(stdin.readline())  # For single input


def In():
    return map(int, stdin.readline().split())  # For multiple input


def L():
    return list(map(int, stdin.readline().split()))  # For array input


def Si():
    return sorted(list(map(int, stdin.readline().split())))  # For sorted array


def Si():
    # For sorted array(in reverse order)
    return sorted(list(map(int, stdin.readline().split())), reverse=True)


def P(x):
    return stdout.write(str(x)+"\n")  # print without newline


def Pi(x, y):
    return stdout.write(str(x)+" "+str(y))


def solve():
    n = I()
    if(n-10 == 0):
        P("0")
    elif(n-10 == 10):
        P("15")
    else:
        P("4")


if __name__ == "__main__":

    solve()