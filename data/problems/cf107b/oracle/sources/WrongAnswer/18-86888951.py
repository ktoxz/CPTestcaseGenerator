from functools import reduce
def C(n,r):
	if(n<r):
		return 0
	elif(r==0 or r==n):
		return 1
	elif(r>n/2):
		return C(n,n-r)
	else:
		num=1
		for i in range(1,r+1):
			num=(num*(n-i+1))/i
		return num
			


nmh=input().split()
n=int(nmh[0])
m=int(nmh[1])
h=int(nmh[2])
L=list(map(int,input().split()))
s=reduce(lambda x,y:x+y,L)
if(s<n):
	print(-1)
else:
	nr=C(s-1,n-L[h-1])
	dr=C(s-1,n-1)
	pro=1-(nr/dr)
	print(pro)