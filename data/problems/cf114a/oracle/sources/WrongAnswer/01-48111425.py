import math as ma
n=int(input())
m=int(input())
e=ma.log(m,n)
e=int(e)
x=n**e
if x==m:
    print("YES")
    print(e-1)
else:
    print("NO")