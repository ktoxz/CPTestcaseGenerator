n,m=map(int,input().split())
s=0
for i in range(m):
	x,d=map(int,input().split())
	end=x+d*(n-1)
	s+=(x+end)*n/2
print(s/n)