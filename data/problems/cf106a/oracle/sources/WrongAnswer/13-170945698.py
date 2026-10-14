a = input()

k = False

b = input().replace(' ','_')

if b[1] == a:

    k = True

m = '6789TJQKA'

if m.index(b[0]) > m.index(b[3]):
    print('YES')

elif m.index(b[0]) > m.index(b[3]) and k:

    print('YES')

else:
    print('NO')