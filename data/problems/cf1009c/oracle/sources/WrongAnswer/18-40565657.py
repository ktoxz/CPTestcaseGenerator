f=lambda: map(int,input().split())
n,m=f()
sum_max_dist=0.0
for i in range(1,n+1): sum_max_dist+=abs(i-(n+1)//2)
ans=0.0
for i in range(m):
    x,d=f()
    if d>0.0:
        ans+=x*n+sum_max_dist*d
    else:
        ans+=x*n+n*(n-1)//2*d
print(ans/n)