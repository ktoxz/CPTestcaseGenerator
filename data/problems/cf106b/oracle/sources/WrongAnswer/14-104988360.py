a = []
for x in range(int(input())):
	b,c,d,e = map(int,input().split())
	f = (d + b + c) - e
	a.append(f)
g = a
g.sort()
print(a.index(g[-1]))