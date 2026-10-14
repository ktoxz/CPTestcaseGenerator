import math
n, k = map(int, input().split())
a = [int(i) for i in input().split()]
res = 0
for i in a:
    res = math.gcd(res, i)
s = sorted(list({(res*i)%k for i in range(n)}))
print(len(s))
for i in s:
    print(i)