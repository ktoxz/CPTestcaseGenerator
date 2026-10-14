n=int(input())
c=0
a=[int(x) for x in input().split()]
for i in range(n-1,-1,-1):
    if c==0:
        c+=a[i]
    else:
        c+=a[i]-1+a[i+1]
print(c)