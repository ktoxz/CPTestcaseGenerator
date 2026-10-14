n,k=map(int,input().split())
a=[int(x) for x in input().split()]
a.sort()
dic={}
for _ in range(k):
    s=input()
    if s in dic:
        dic[s]+=1
    else:
        dic[s]=1
t=0
cnt=0
sorted(dic.items(),reverse=True)
for i in dic:
    cnt+=a[t]*dic[i]
    t+=1
print(cnt,end=" ")
t=n-1
cnt=0
for i in dic:
    cnt+=a[t]*dic[i]
    t-=1
print(cnt)