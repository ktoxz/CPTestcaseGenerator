def f(k, x):
    return (m + x) / k
def g(c):
    for i in range(n):
        c -= f(a[i], c)
        c -= f(b[i], c)
    return c
I = input
n, m, l, r = int(I()), int(I()), 0, 1e9
*a, = map(int, I().split())
*b, = map(int, I().split())
if g(1e9) < 0:
    print(-1)
    exit()
while r - l > 1e-6:
    w = (r + l) / 2
    #print(l, w, r)
    c = g(w)
    if c > 0: r = w
    elif c < 0: l = w
    else:
        print(w)
        exit()
print(w)