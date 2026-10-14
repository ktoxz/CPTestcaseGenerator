n, m = [int(i) for i in input().split()]
x = 0
d = 0
for i in range(m):
    a, b = [int(i) for i in input().split()]
    x += a
    d += b
t = [0.5 * ((n-1-j)*(n-j) + j*(j+1)) for j in range(n)]
if d <= 0:
    print(x + d * min(t) / n)
else:
    print(x + d * max(t) / n)