def comb(n,m):
    return fact(n)//fact(n-m)//fact(m)
def fact(n):
    s =1
    for i in range(1,n+1):
        s*=i
    return s;
n,m,h = map(int,input().split())
a = list(map(int,input().split()))
n-=1
a[h-1]-=1;
s =0
for i in a:
    s+=i
if(a[h-1]==0 or s<n):
    print(-1)
else:
    print((comb(s,n)-comb(s-a[h-1],n))/comb(s,n))