n,d = map(int,input().split())
l = list(map(int,input().split()))
c=0
for i in range(1,n):
    if(l[i]<=l[i-1]):
        a = l[i-1]-l[i]
        l[i]+=d*(a+1)
        c+=1
print(c)