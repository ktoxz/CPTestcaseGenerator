n, m = int(input()), int(input())
a = []
x = 0
while n:
    d = n % 10
    if d == 0:
        x += 1
    else:
        a.append(d)
    n //= 10
a = [a[0]] + [0] * x + a[1:]
if ''.join(map(str, a)) == str(m):
    print('OK')
else:
    print('WRONG_ANSWER')