from sys import stdin
def input(): return stdin.readline()[:-1]
s=input()
h=int(s[0:2])
m=int(s[3:])
for i in range(1000):
	m+=1
	if m==60:
		h+=1
		if h==24:
			h=0
		m=0
	s=str(h).zfill(2)+":"+str(m).zfill(2)
	if s==s[::-1]:
		print(s)
		break