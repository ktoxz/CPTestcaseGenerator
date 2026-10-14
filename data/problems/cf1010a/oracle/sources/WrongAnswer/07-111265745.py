def bs(l, h):
    while (h - l > 10 ** -6):
        m = (l + h) / 2
        if gf(m):
            h = m
        else:
            l = m + 10 ** -6
    return l

def gf(x):
    x -= (m + x) / a[0]
    for i in range(1, n):
        x -= (m + x) / b[i]
        x -= (m + x) / a[i]
    x -= (m + x) / b[0]
    return x >= 0

n = int(input())
m = int(input())
a = tuple(map(int, input().split()))
b = tuple(map(int, input().split()))
x = bs(0, 10 ** 9)
print(x) if x <= 10 ** 9 else print(-1)