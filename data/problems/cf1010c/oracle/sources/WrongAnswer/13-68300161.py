n, k = map(int, input().split())
a = list(map(int, input().split()))
ans = set()
ans.add(0)
for i in a:
	ans.add(i % k)
print(len(ans))
print(*sorted(list(ans)))