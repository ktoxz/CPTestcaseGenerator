n,m,k=list(map(str,input().split()))
n=int(n);m=int(m);k=float(k)
l={}
from math import *;
for x in range(n):
    ap=list(map(str,input().split()))
    if (floor(int(ap[1])*k)>=100):
        l[ap[0]]=floor(int(ap[1])*k)
r=list(l.keys())
for y in range(m):
    xy=input()
    if (xy not in r):
        l[xy]=0
rp=sorted(l)
print(len(rp))
for a in rp:
    print(str(a)+' '+str(l[a]))