import math
from collections import defaultdict, Counter, deque

INF = float('inf')

def gcd(a, b):
	while b:
		a, b = b, a%b
	return a


def primeFactor(n):
	if n % 2 == 0:
		return 2
	i = 3
	while (i ** 2) <= n:
		if n % i == 0:
			return i 
		i += 1
	return n

def main():
	n = int(input())

	queen = 10

	req = n - 10
	ans = 0
	if req <= 0 or req > 21:
		print(ans)
	else:
		if req == 11:
			ans += 4
		elif req == 10:
			ans += 4 + 4 + 3 + 4
		elif ans == 1:
			ans += 8
		else:
			ans += 4
		print(ans)

	





	

if __name__ == "__main__":
	# t = int(input())
	t = 1
	for _ in range(t):
		main()