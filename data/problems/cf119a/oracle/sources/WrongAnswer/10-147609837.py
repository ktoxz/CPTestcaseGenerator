def gcd(a, b):
	afac = [(i, a//i) for i in range(1, int(a**0.5) + 1) if a % i == 0]
	afac = [i for sub in afac for i in sub][::-1]
	bfac = [(i, b//i) for i in range(1, int(b**0.5) + 1) if b % i == 0]
	bfac = [i for sub in bfac for i in sub][::-1]
	found = False
	for ai in afac:
		for bi in bfac:
			if ai == bi:
				found = True
				break
		if found: break
	return ai

a, b, h = input().split()
a, b, h = int(a), int(b), int(h)
i = 0
while h:
    if i % 2 == 0: 
        h -= gcd(a, h)
        ans = "0"
    else: 
        h -= gcd(b, h)
        ans = "1"
    i += 1
print(ans)