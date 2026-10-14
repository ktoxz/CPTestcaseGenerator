n, m = map(int, input().split())
k, x, y = 0, (n - 1) / 2, ((n // 2 - 1) * (n // 2) / 2 + (n - n // 2 + 1) * (n - n // 2) / 2) / n
for i in range(m):
	a, b = map(int, input().split())
	k += a + (b * (x if b > 0 else y))
print(k)