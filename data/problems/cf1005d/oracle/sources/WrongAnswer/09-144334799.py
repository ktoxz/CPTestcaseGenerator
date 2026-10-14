from collections import  defaultdict

bad=[]
for i in range(0,10**6,3):
    if len(str(i))==1:
        bad.append(str(i))
    else:
        s=str(i)
        fl=False
        for j in bad:
            if j in  s:
                fl=True
                break
        if not  fl:
            bad.append(s)

# bad=list(map(int,bad))

s=list(input())
res=""
ans=0
for id,i in enumerate(s):
    if i in bad:
        ans+=1
        continue
    if id+1<len(s):
        if i+s[id+1] in bad:
            ans+=1
            s[id+1]='.'
            continue
    if id+2<len(s):
        if i+s[id+1]+s[id+2] in bad:
            ans+=1
            s[id+1]="."
            s[id+1]="."
            continue
print(ans)