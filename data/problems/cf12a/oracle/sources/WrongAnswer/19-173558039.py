n,z=3,[]
c=0
for i in range(n):
	x=input()
	z.append(list(x))
for i in range(1):
	for j in range(1):
		if z[i][j]!=z[2-i][2-j]:
			c=1
			break
if c==0:
	print("YES")
else:
	print("NO")