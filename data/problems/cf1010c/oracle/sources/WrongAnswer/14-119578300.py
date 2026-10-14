import sys
from math import gcd
input=sys.stdin.readline
n,k=map(int,input().split())
a=list(map(int,input().split()))
g=a[0]
for i in range(1,n):
    g=gcd(g,a[i])
s=set()
val=g
for i in range(10**7):
    s.add(val)
    val*=g
    val%=k
print(len(s))
print(*list(s))