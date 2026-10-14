import math
n=int(input())
nlist=list(map(int,input().split()))
m=int(math.log(10**9,2))
dicc={}
for x in nlist:
    dicc[x]=dicc.get(x,0)+1
ans=0
for x in dicc:
    for i in range(m+1):
        flag=0
        if 2**i-x==x:
           if dicc[x]>1:
               flag=1
               break
        elif 2**i-x in dicc:
            flag=1
            break
    if flag==0:
        ans+=1
print(ans)