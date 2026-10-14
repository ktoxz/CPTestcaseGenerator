import sys
input = lambda: sys.stdin.readline().rstrip()
import math
from heapq import heappush , heappop
from collections import defaultdict,deque,Counter
from bisect import *

N = int(input())
S = input()
T = input()

def check(C):
    keys = list(C.keys())
    if len(keys)>2:
        return False
    if len(keys)==1:
        return True
    if C[keys[0]]==C[keys[1]]:
        return True
    return False

def cal(A):
    t = int(A[0]!=A[2]) + int(A[1]!=A[3])
    t = min(t, int(A[0]!=A[3]) + int(A[1]!=A[2]))
    return t
    
ans = 0
for i in range(N//2):
    j = N-i-1
    #print(i,j,S[i],S[j])
    tmp = [S[i],S[j],T[i],T[j]]
    C = Counter(tmp)
    if check(C):
        continue
        
    ans += cal(tmp)
if N%2:
    #print(N//2+1)
    if S[N//2]!=T[N//2]:
        ans+=1
    
print(ans)