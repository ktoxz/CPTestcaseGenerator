n = int(input())
m = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

def canFly(c):
	c += m
	for i in range(n):
		if i != 0:  # 先降落
			cost = c / b[i]
			c -= cost
		if i != n-1: # 起飞
			cost = c / a[i]
			c -= cost
		if c <= m: return False
		
	cost = c / a[n-1]
	c -= cost
	cost = c / b[0]
	c -= cost 
	if c < m: return False
	return True

l,r = 1, 10**9
while abs(l-r) > 10**-6:
	mid = (l+r) / 2
	if canFly(mid):
		r = mid
	else:
		l = mid
print(l)