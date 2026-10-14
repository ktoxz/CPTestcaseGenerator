a=int(input())
b=int(input())

s=list(str(a))
s.sort()

c=s.count('0')
while(True):
	if(s[0]=='0'):
		s.pop(0)
	else:
		break
ans=int(''.join(s))

if(ans==b):
	print("OK")
else:
	print("WRONG_ANSWER")