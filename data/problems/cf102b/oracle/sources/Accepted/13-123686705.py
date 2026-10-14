from sys import *
input = lambda:stdin.readline()

int_arr = lambda : list(map(int,stdin.readline().strip().split()))
str_arr = lambda :list(map(str,stdin.readline().split()))
get_str = lambda : map(str,stdin.readline().strip().split())
get_int = lambda: map(int,stdin.readline().strip().split())
get_float = lambda : map(float,stdin.readline().strip().split())


mod = 1000000007
setrecursionlimit(1000)

n = str(input())[:-1]
ct = 0
while len(n) > 1:
    tot = 0
    for i in n:
        tot += int(i)
    n = str(tot)
    ct += 1
print(ct)