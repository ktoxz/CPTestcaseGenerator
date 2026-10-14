k=int(input())
l=int(input())
flag=0
la=0
while k<=l:
    k*=k
    la+=1
    if k==l:
        flag=1

if flag==1:
    print('YES')
    print(la)
else:
    print('NO')