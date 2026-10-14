a=[]
b=[]
for i in range(3):
    n=input()
    n.split()
    for j in n:
        a.append(j)
for k in range(8,0,-1):
    b.append(a[k])
b.append(a[0])
print(a,b)
if a==b:
    print('YES')
else:
    print('NO')