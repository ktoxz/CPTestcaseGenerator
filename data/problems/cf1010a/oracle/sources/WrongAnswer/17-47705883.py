n=int(input())
m=int(input())
a=list(map(int,input().split()))
b=list(map(int,input().split()))
def c(x):
    x-=(m+x)/a[0]
    for i in range(1,n):
        x-=(m+x)/b[i]
        if x<0: return False
        x-=(m+x)/a[i]
        if x<0: return False
    x-=(m+x)/b[0]
    return x>=0

l,r=0,10**9+1
x=0
for i in range(100):
    x=(l+r)/2
    if c(x):
        r=x
    else:
        l=x
if c(x):print(x)
else: print(-1)