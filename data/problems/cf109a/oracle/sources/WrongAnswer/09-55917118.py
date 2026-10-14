n=int(input())
if(n%4==0 and n%7!=0):
	print ((n//4)*'4')
elif n%4!=0 and n%7==0:
	print ((n//7)*'7')
else:
	k=(n//7)*'7'
	n=n%7
	p=((n)//4)*'4'
	if(n%4==0):
		print(p,end="")
		print(k)
	else:
		print(-1)