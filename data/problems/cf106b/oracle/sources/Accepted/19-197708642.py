I=input
n=int(I())
r=list(tuple(map(int,I().split()))for _ in '0'*n)
s=set(r)
d=set()
for a in s:
	for b in s:
		y=1
		for i in 0,1,2:y=y and a[i]<b[i]
		if y:break
	else:d.add(a)
print(1+r.index(sorted(d,key=lambda x:x[-1])[0]))