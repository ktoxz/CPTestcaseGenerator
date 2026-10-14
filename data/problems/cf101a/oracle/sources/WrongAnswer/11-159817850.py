s=input("")
d=dict()
k=int(input())
b=s 
setS=set()
for i in s:
    if i not in setS:
        d.update({i:s.count(i)})
        setS.update(i)
cnt=0
for i,j in d.items():
    if j<=k:
        b=b.replace(i,"")
cnt=len(set(b))
print(cnt)
print(b)