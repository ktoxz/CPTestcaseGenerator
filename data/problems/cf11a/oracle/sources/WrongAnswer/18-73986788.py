l=list(map(int,input().split()))
n=l[0]
d=l[1]
a=[0]*n
c=0
l=input()
l=list(map(int,l.split()))
for i in range(0,n):
    a[i]=int(l[i])
    if i == 0:
        continue
    if a[i] < a[i-1]:
        c+=1
        a[i]=a[i]+d
print(c)