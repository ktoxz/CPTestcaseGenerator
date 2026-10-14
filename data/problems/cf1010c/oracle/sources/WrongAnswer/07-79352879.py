import sys
n,k=map(int,sys.stdin.readline().split())
a=list(map(int,sys.stdin.readline().split()))
l=[0 for _ in range(n)]
for i in range(n):
    l[i]=a[i]%k
ans=set()
ans.add(0)
for i in range(n):
    if l[i]!=0:
        if k%l[i]!=0:
            for j in range(0,k):
                ans.add(j)
            print(k)
            print(*list(ans))
            sys.exit()
        else:
            st=0
            while st*l[i]<k:
                ans.add(st*l[i])
                st+=1
print(len(ans))
print(*list(ans))