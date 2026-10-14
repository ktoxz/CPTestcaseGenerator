n,m=input().split()
n,m=int(n),int(m)
c=0
z=0
for j in range(n):
    c+=j
    z+=abs(n//2-j)
s=0
for i in range(m):
    x=[int(x) for x in input().split()]
    s+=x[0]*n+max(x[1]*z,x[1]*c)
print(s/n)