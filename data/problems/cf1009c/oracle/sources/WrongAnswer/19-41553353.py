n,m = list(map(int, input().split()))
ans = 0
for i in range(m):
    x,d = list(map(int, input().split()))
    ans += x*n
    if d >= 0:
        ans+= (n-1)*n*d/2
    else:
        a = int(n/2)
        if n%2 == 1:
            ans+= d*a*(a+1)
        else:
            ans+= (a**2)*d
print(ans/n)