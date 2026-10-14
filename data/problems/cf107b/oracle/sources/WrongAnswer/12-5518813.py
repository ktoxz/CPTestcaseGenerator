n, m, h = map(int, input().split())
s = list(map(int, input().split()))
n, h = n - 1, h - 1
a, b = sum(s) - s[h], s[h] - 1
if a < n: print(-1 if a + b < n else 1)
else:
    p = q = 1
    for i in range(a - n + 1, a + 1): p *= i
    for i in range(a + b + 1, a + b + n + 1): q *= i
    print(1 - q / p)