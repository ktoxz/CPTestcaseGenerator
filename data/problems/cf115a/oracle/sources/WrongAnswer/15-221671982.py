from math import*
n=int(input())
q=[]
for i in range(n):
    a=int(input()) 
    if a not in q:
        q.append(a)
print(len(q))