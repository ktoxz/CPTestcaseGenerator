L=[]
for i in range(0,3):
    L.append(list(input()))
flag=0
for i in range(0,3):
    for j in range(0,3-i):
        if L[i][j]!=L[2-i][2-j]:
            flag=1
            break
    if flag==1:
        break
if flag==1:
    print("NO")
else:
    print("YES")