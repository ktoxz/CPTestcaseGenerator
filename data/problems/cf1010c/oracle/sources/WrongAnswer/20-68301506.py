n, k = map(int, input().split())
a = list(map(int, input().split()))
ans = set()
for x in a:
	o = 0
	while x > k:
		o = x%k
		x//=k
	ans.add(o)
a = list(sorted(ans))
for i in range(len(a)):
	for j in range(i , len(a)):
		ans.add((a[i]+a[j])%k)
		
print(len(ans))
print(*(sorted(ans)))