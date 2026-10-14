a = list(input())
b = int(input())


u=[]
for k in set(a):
    u.append([a.count(k),k])

u.sort()


x=len(u)

for k  in range(x):
    if b>u[k][0]:
        b-=u[k][0]
        u[k][0]=0
    else:
        break
    



f=''
y=0
for j in u:
    f+=j[1]*j[0]
    if j[0]>0:
        y+=1

print(y)
print(f)