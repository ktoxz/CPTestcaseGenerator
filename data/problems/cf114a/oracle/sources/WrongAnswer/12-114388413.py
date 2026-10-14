k = int(input())
l = int(input())
c = 0
while k < l:
    k *= k
    c += 1
if k == l:
    print('YES')
    print(c)
else:
    print('NO')