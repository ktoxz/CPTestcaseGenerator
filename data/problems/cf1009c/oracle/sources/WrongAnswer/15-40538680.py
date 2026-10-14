n,m=map(int,(input().split()))
p=0;
for i in range(1,n+1): p+=abs(i-(n+1)/2)
ans=0
for i in range(m):
    x,d=map(int,(input().split()))
    sum=n*x+max(d*(n*(n-1)/2),d*p)
    ans+=sum
out=1.0*ans/n
print("%0.10f"%out)