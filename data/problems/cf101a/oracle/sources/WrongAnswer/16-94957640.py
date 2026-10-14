import collections
s=input()
k=int(input())

d=dict()
for i in s:
 if i in d:d[i]+=1
 else:d[i]=1
d=sorted(d.items(), key=lambda x: x[1])
A=set()
ans=0
for i  in d:
 if k-i[1]>0:
   A.add(i[0])
   k-=i[1]
   ans+=1
print(len(d)-ans)
for i in s:
 if i not in A:
   print(i,end="")