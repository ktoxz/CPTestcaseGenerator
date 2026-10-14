# cook your dish here
n,k=map(int,input().split())
l=list(map(int,input().split()))
a=1
c=k*k
j=1
for i in range(1,n+1):
    b=a+l[i-1]-1
    c-=l[i-1]
    if c>=0 and b<=k:
        print(j,a,b)
        a=b+1
    elif c>=0 and b>k:
        j+=1
        a=1
        b=a+l[i-1]-1
        print(j,a,b)
        a=b+1
    else:
        print(-1)