n,p1,p2,p3,t1,t2=list(map(int,input().split()))
r1=-1
e=0
for i in range(n):
    l,r=list(map(int,input().split()))
    e+=(r-l)*p1
    if r1!=-1:
        e+=p1*min(t1,l-r1)+p2*max(0,min(l-r1-t1,t2))+p3*max(0,l-r1-t1-t2)
    r1=r
print(e)