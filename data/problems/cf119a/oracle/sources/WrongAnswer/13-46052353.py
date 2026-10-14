import math
a, b, n = map(int,input().split())
i = 0
print(math.gcd(5,0))
while n > 0:
    n = n - math.gcd(a, n)
    n = n - math.gcd(b, n)
    i = i+1
print([0, 1][i%2==0])