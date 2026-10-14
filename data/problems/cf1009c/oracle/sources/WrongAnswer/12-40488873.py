n, m = [int(i) for i in input().split()]
x = 0
d = 0
for i in range(m):
    a, b = [int(i) for i in input().split()]
    x += a
    d += b
if d < 0:
    print(x + d * 0.5 * (n / 2 + 1))
else:
    print(x + d * 0.5 * (n - 1))