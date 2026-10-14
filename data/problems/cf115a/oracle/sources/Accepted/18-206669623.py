n=int(input())
s,t=[int(input())for i in range(n)],0
for i in range(n):
	c=0
	while i>=0:i=s[i]-1;c+=1
	t=max(t,c)
print(t)