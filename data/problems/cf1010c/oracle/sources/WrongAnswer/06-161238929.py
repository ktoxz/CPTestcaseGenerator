import math
n,k = [int(i) for i in input().split()]
g = 0
for i in input().split(): g = math.gcd(g,int(i)%k)
if(g==0):
    print(1)
    print(0)
else:
    x = k//g
    A = []
    for i in range(1,x+1): A.append((g*i)%k)
    A.sort()
    print(x)
    print(*A,sep=' ')