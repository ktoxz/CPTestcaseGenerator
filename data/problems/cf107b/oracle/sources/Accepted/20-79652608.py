n, m, h = map(int, input().split())
s = list(map(int, input().split()))
t = sum(s)
if n > t: print(-1)
elif s[h-1] == 1: print(0)
elif t - s[h-1] + 1 < n: print(1)
else:
	a = t-s[h-1]
	b = t-1
	c = b-n+1
	d = a-n+1
	z = 1
	for i in range(a+1,b+1):
		z *= i
	y = 1
	for i in range(d+1,c+1):
		y *= i
	print(1-(y/z))