n, p1, p2, p3, t1, t2 = map(int, input().split())
result = b = time = 0
for i in range(n):
	l, r = map(int, input().split())
	phase = 1
	while time!=l and i!=0:
		if phase==1:
			if l-time<t1:
				result+=(l-time)*p1
				time+=(l-time)
			else:
				result+=t1*p1
				phase=2
				time+=t1
		elif phase==2:
			if l-time<t2:
				result+=(l-time)*p2
				time+=(l-time)
				phase=1
			else:
				result+=t2*p2
				phase=3
				time+=t2
		else:
			result+=(l-time)*p3
			time+=(l-time)
			phase=1
	result+=(r-l)*p1
	time = r
print(result)