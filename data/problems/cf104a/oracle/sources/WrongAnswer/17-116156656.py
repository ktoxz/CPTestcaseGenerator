import math

def solve(n):
    n = n - 10
    if n in [1,11]:
        return 4
    if n in [2,3,4,5,6,7,8,9]:
        return 4
    if n == 10:
        return 15

n = int(input())
# a = input()
# b = input()

print(0) if n == 10 else print(solve(n))