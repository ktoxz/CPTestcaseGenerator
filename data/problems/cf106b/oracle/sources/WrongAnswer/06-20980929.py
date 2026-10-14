I=input
n=int(I())
a=[list(map(int,I().split()))for _ in '0'*n]
t=0
for i in range(n):
	x=y=1
	for j in 0,1,2:y=y and a[t][j]<a[i][j];x=x and a[t][j]>a[i][j]
	if 1-x and a[t][3]>a[i][3]or y:t=i
print(t)