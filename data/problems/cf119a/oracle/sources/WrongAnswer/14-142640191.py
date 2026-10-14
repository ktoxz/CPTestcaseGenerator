def nod(x, y):
    while y > 0:
        x, y = y, x % y
    return x

a, b, n = map(int, input().split())
z = 0
while True:
    if z % 2 == 0:
        num_needed = nod(b, n)
        if n < num_needed:
            print(1)
            break
        else:
            n -= num_needed
    else:
        num_needed = nod(a, n)
        if n < num_needed:
            print('0')
            break
        else:
            n -= num_needed
    z += 1