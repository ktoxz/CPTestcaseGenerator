import math
a,b,n=map(int,input().split())
x=0
y=0
while n>0:
	n = n - math.gcd(n,a)
	if n<=0:
		x=1
		break
	else:
		n = n- math.gcd(n,b)
		if n<=0:
			y=1
			break
if x==1:
	print(0)
elif y==1:
	print(1)