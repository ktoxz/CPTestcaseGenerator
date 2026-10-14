n, k = map(int, input().split())
a = list(map(int, input().split()))
ans = set()
for x in a:
	o = 0
	while x > k:
		o = x%k
		x//=k
	ans.add(o)
	if k % 2 == 0 and k // 2 == o:
		ans.add(0)
	if o == 1:
		print(k)
		print(*range(k))
		exit()
	if k%2 != o%2:
		print(k)
		print(*range(k))
		exit()

a = list(sorted(ans))
for i in range(len(a)):
	for j in range(i , len(a)):
		ans.add((a[i]+a[j])%k)
		
print(len(ans))
print(*(sorted(ans)))