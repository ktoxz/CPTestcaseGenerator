n, m, h = map(int, input().split())
a = list(map(int, input().split()))
s = sum(a) - a[h - 1]

if (sum(a) < n):
    print(-1)
    exit()

s = sum(a)- a[h - 1]

if (s < n - 1):
    print(0)
    exit()

x, y = 1, 1
for i in range(s - n + 2, s + 1):
    x *= i

for i in range(s + a[h - 1] - n + 1, s + a[h - 1]):
    y *= i

print(1 - x/y)