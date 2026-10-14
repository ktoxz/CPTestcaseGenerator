n,m,k=input().split()
n,m=int(n),int(m)
k=int(k[2:])
d={}
d2={}
ans=[]
for i in range(n):
	a,b=input().split()
	# print ((int(b)*int(str(k)[2:]))/100)
	# print ((int(b)),str(k),str(k)[2:],int(str(k)[2:]),int(b)*int(str(k)[2:]),int(b)*int(str(k)[2:]))
	if (int(b)*k/100)>=100:
		d[a]=int(b)*k/100
for i in range(m):
	s=input()
	d2[s]=0
for i in d:
	ans.append((i,d[i]))
for i in d2:
	if i not in d:
		ans.append((i,d2[i]))
ans.sort()
print (len(ans))
for i in ans:
	print (i[0],int(i[1]))