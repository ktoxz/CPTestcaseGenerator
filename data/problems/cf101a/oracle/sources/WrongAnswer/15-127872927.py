from collections import Counter
l=Counter(input())
s=sorted(l.items(), key=lambda kv: kv[1],reverse=True)
p=sum(l.values())-int(input())
to=0;ans=''
for x in s:
    if p<1: break
    p-=x[1]
    to+=1
    ans+=x[0]*x[1]
print(to)
print(ans)