n,m=map(int,input().split())
k=n//2
ans=0
for _ in range(m):
    x,d=map(int,input().split())
    if d>0:
        ans+=(x*n+d*n*(n-1)/2)/n
    else:
        if n&1:
            ans+=(x*n+d*k*(k+1))/n
        else:
            ans+=(x*n+d*k*k)/n
print(ans)