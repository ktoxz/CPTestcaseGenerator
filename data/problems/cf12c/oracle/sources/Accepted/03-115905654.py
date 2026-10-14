n,m=map(int,input().split())
a=sorted(map(int,input().split()))
q={}
for i in range(m):
    o=input()
    if o in q:q[o]+=1
    else:q[o]=1
w=sorted(q[i] for i in q)[::-1]
e,r=0,0
for i in range(len(w)):
    e+=w[i]*a[i]
    r+=w[i]*a[n-1-i]
print(e,r)