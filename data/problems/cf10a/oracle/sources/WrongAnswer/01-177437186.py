n=input()
yes=0
no=0
for x in n:
    if x=='4' or x=='7':
        yes+=1
    else:
        no+=1
if no==0:
    print('YES')
else:
    print('NO')