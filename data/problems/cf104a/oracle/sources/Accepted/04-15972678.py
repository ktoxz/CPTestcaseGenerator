n = int(input())

if (n-10)<=0:
	print(0)
elif (n-10)>0 and (n-10)<=11:
	if (n-10)==10:
		print(15)
	else:
		print(4)
else:
	print(0)