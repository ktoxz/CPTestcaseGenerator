n = int(input())
l=[]
for i in range(n):
	l.append(int(input()))
m=0
for i in range(n):
	c=0
	ind=i
	while ind>=0:
		ind=l[ind]-1
		c+=1
	m=max(m,c)
print(m)