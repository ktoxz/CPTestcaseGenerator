a=input().split()
n,m,k=int(a[0]),int(a[1]),float(a[2])
b={}
for _ in range(n):
    a=input().split()
    c=int(a[1])*k
    if c>100: b[a[0]]=c
for _ in range(m):
    d=input()
    if not (d in b): b[d]=0
print(len(b))
for e in sorted(b):
    print(e,b[e])