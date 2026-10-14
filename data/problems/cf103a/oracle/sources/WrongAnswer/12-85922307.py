import sys
def input():
    return sys.stdin.readline().strip()
 
 
def iinput():
    return int(input())
 
 
def tinput():
    return input().split()
 
 
def rinput():
    return map(int, tinput())
 
 
def rlinput():
    return list(rinput())

n = iinput()
A = rlinput()
ans = 0
for i in range(n):
    if A[i] != 1:
        ans += A[i] + i
    else:
        ans += 1
print(ans)