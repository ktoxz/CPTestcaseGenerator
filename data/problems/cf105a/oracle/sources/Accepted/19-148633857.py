n,m,k=map(float,input().split())
n,m,k=round(n),round(m),round(k*100)
D=dict()
for i in range(n):
    x=input().split()
    F=int(x[1])*k//100
    if(F>=100):
        D[x[0]]=F
 
for i in range(m):
    x=input()
    if x not in D:D[x]=0
print(len(D))
for x in sorted(D):
    print(x,D[x])