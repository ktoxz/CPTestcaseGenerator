n=input()
c=0
while len(n)>1:
	s=0
	for i in n:
		s+=int(i)
	n=str(s)
	c+=1
print(c)