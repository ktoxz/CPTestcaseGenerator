def pos(a,b,f,fuel):
	i=0
	flag=0
	while flag==0:
		f-=(f/a[i])
		i+=1
		if i==len(a):
			flag=1
			i=0
		f-=(f/b[i])
	return f>=fuel
n=float(input())
init=float(input())
a=list(map(float,input().split()))
b=list(map(float,input().split()))
lo=0
hi=2000
ans=100000000000
# print(pos(a,b,22,12))
while lo<hi:
	mid=(lo+hi)/2
	if pos(a,b,init+mid,init):
		if (abs(mid-ans)/mid)<10**(-12):
			break
		ans=min(ans,mid)
		hi=mid
	else:
		lo=mid
if ans==100000000000:
	print(-1)
else:
	print(ans)