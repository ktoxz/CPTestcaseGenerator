import sys
input = lambda: sys.stdin.readline().rstrip()
import math

N,M,H = map(int, input().split())
A = list(map(int, input().split()))

total = sum(A)
if total<N:
    exit(print(-1))

total-=1
t1 = math.comb(total,N-1)

total=sum(A)-A[H-1]
t2 = math.comb(total,N-1)
print(1-t2/t1)