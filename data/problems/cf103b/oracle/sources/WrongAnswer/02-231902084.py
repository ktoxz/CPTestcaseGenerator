def find(x):
    if x!=s[x]:s[x]=find(s[x])
    return s[x]
def merge(x,y):
    x=find(x)
    y=find(y)
    if x!=y:
        s[x]=s[y]
m,n=map(int,input().split())
s=list(range(m+1))
if m!=n:
    print("NO")
else:
    for i in range(m):
        a,b=map(int,input().split())
        merge(a,b)
    for i in range(1,m):
        if find(i)!=find(i+1):
            print("NO")
            break
    else:
        print("FHTAGN")