n = int(input())
l = list(map(int,input().split()))
s = 0

for i in range(n):

	s = s + i*(l[i]-1) + l[i]
print(s)