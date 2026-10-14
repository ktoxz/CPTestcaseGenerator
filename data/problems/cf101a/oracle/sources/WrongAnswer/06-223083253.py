angka=input()
b=0
for i in angka:
    if i == '4' or i=='7':
        b=b+1
if b==4 or b==7:
    print('YES')
else:
    print('NO')