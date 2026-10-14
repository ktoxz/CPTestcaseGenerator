n=int(input())

a=str(input())

b=str(input())
ans=0
if n%2==1:
	if a[n//2]!=b[n//2]:
		ans+=1
def aze(l):
	l=[ord(i)-ord("a") for i in l]
	d=set(l)
	f=[l.count(i) for i in d]
	if len(f)>=3:
		return(2)
	elif len(f)==2:
		if 1 in f:
			return(1)
		return(0)
	return(0)

	


for i in range(n//2):

	ans+=aze(a[i]+a[n-1-i]+b[i]+b[n-1-i])
	
print(ans )