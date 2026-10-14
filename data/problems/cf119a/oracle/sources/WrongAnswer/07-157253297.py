from math import gcd
a,b,n=map(int,input().split())
i=0
while(n>0):
    if(i%2==0):
        n=n-gcd(a,n)
    else:
        n=n-gcd(b,n)
    i=i+1
if(i%2==0):
    print(0)
else:
    print(1)