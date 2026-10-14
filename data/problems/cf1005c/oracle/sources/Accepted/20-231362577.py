n=int(input())
ll=list(map(int,input().split()))
ll.sort()
o,e=dict(),dict()
kk=[]
i=2
x=1
while i<10**9:
    i=2**x
    x+=1
    kk.append(i)
for i in ll:
    if i&1:
        if i in o:
            o[i]+=1
        else:
            o[i]=1
    else:
        if i in e:
            e[i]+=1
        else:
            e[i]=1
for i in kk:
    if i==2:
        if 1 in o and o[1]>1:
            o[1]=True
    else:
        x=i//2
        if x in e and e[x]>1:
            e[x]=True

for i in o:
    if isinstance(o[i],int):
        x=i
        for t in kk:
            if x<t:
                f=t-x
                if x!=f and f in o:
                    o[f]=True
                    o[x]=True
for i in e:
    if isinstance(e[i],int):
        x=i
        for t in kk:
            if x<t:
                f=t-x
                if x!=f and f in e:
                    e[f]=True
                    e[x]=True
c=0
for i in o:
    if not isinstance(o[i],bool):
        c+=o[i]
for i in e:
    if not isinstance(e[i],bool):
        c+=e[i]
print(c)