n,m = map(int,input().split())


t = list(map(int,input().split()))
f=[]

for k in range(m):
    f.append(input())

l=[]

for k in set(f):
    l.append([f.count(k),k])

l.sort()
L=l[::-1]
t.sort()

p=0
q=0
for h in range(len(l)):
    p+=L[h][0]*t[h]
    q+=L[h][0]*t[-(h+1)]


print(p,q)