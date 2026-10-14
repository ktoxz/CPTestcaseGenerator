import math
n,d=map(int,input().split())
a=list(map(int,input().split()))
c=0
for i in range(len(a)-1):
	if(a[i+1]<=a[i]):
		if((a[i]-a[i+1])<d):
			a[i+1]=a[i+1]+d
			c=c+1
		else:
			x=int(math.ceil((a[i]-a[i+1])/d))
			a[i+1]=a[i+1]+x*d
			c=c+x
print(c)