a=str(input())
b,c=map(str,input().split())
if b[0]=='6':
    z1=6
if b[0]=='7':
    z1=7
if b[0]=='8':
    z1=8
if b[0]=='9':
    z1=9
if b[0]=='T':
    z1=10
if b[0]=='J':
    z1=11
if b[0]=='Q':
    z1=12
if b[0]=='K':
    z1=13
if b[0]=='A':
    z1=14
if c[0]=='6':
    z2=6
if c[0]=='7':
    z2=7
if c[0]=='8':
    z2=8
if c[0]=='9':
    z2=9
if c[0]=='T':
    z2=10
if c[0]=='J':
    z2=11
if c[0]=='Q':
    z2=12
if c[0]=='K':
    z2=13
if c[0]=='A':
    z2=14
if z1>=z2:
    if b[1]==a:
        print('YES')
    elif b[1]==c[1]:
        print('YES')
    else:
        print('NO')
else:
    print('NO')