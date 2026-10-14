n,p=map(int,input().split())
a=[[0,0,0] for _ in range(n+1)]
for _ in range(p):
    s,f,d=map(int,input().split())
    a[s][0]=f #kuda
    a[f][1]=s #otcuda
    a[s][2]=d #skolko
ans=[]
for i in range(1,n+1):
    if a[i][1]!=0:continue # find start (bak)
    f=a[i][0]
    s=i
    d=a[s][2]
    if f==0:continue
    while f>0:
        d=min(d,a[s][2])
        s=f
        f=a[s][0]
    ans.append(str(i)+' '+str(s)+' '+str(d))
print(len(ans))
print('\n'.join(ans))