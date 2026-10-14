n,m,k=input().split()
n=int(n);m=int(m);k=float(k)
ans=[];re=[]
for i in range(n):
    x,y = input().split()
    if int(int(y)*k) > 99 :
        ans.append([x , int(int(y)*k)])
        re.append(x)
for j in range(m):
    c=input()
    if c not in re :
        ans.append([c,0])
ans.sort()        
print(len(ans))        
for s,i in ans:
    print(s,i)