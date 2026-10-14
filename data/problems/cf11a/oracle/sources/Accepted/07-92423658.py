from math import *
n,k=map(int,input().split())
l=list(map(int,input().split()))
c=0
for i in range(n-1):
    if(l[i]>l[i+1]):
        d=abs(l[i+1]-l[i])+1
        x=ceil(d/k)
        c=c+x
        l[i+1]=l[i+1]+(x*k)
    elif(l[i]==l[i+1]):
        c+=1
        l[i+1]=l[i]+k
print(c)