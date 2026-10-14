am, ai, bx, bi, cx, ci = 0, 0, 0, 0, 0, 0
x = [0]*3
for i in range(int(input())):
	a,b,c,d = map(int, input().split())
	if a>am:
		x[0]= i
		am=a
		ai= d
	elif a==am and d < ai:
		ai=d
		x[0]= i
	if b>bx:
		x[1]= i
		bx=b
		bi= d
	elif b==bx and d<bi:
		bi=d
		x[1]= i
	if c>cx:
		x[2]= i
		cx=c
		ci= d
	elif c==cx and d<ci:
		x[2]= i
		ci=d	
m  = min(ai,bi,ci)
if m == ai:
	ans = x[0]
elif m== bi:
	ans = x[1]
else:
	ans = x[2]
	
print(ans+1)