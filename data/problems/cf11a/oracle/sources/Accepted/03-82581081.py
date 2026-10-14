n, d = map(int, input().split())
l = list(map(int, input().split()))
ans = 0
for i in range(n-1):
	if l[i] >= l[i+1]:
		x = ((l[i]-l[i+1])//d)+1
		ans += x
		l[i+1] += d*x
print(ans)