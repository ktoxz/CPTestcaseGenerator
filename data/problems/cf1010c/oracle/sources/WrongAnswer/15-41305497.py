import math
from functools import reduce
a,b = map(int,input().split())
c = list(map(int,input().split()))
d = reduce((lambda x, y: math.gcd(x,y)),c)
e = math.gcd(d,b)
print(b//e)
f = ""
for i in range(0,b,e):
    f = f + str(i) + ""
print(f[:-1])