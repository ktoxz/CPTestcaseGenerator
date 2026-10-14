import math as M
n,k=list(int(i) for i in input().split())
A=list(int(i) for i in input().split())
B=[]
if(n>=2):
    g=M.gcd(A[0],A[1])
else:
    g=A[0]
for i in range(n):
    g=M.gcd(A[i],g)
for j in range(k+1):
    d=(g*j)%k
    if d not in B:
            B.append(d)
#B.sort()
print(len(B))
print(*B)