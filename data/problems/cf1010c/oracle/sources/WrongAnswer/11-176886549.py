import math
n, k = map(int, input().split())
g = 0
a = list(map(int, input().split()))
for i in range(n):
    g = math.gcd(a[i], g)
ans = set()
s = 0
for i in range(k):
    ans.add(s%k)
    s+=g
print(len(ans));
print(*ans)