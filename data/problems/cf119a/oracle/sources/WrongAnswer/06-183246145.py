import math
a,b,n=map(int,input().split())
p=True
while(n!=0):
    x=a if p else b
    n-=math.gcd(a,b)
    p=not p
print(p)