n, m = [int(i) for i in input().split()]
mi = (n // 2) * (n // 2 + 1) / n - ((n + 1) % 2) * ((n // 2) / n)
ma = (n - 1) // 2
avg = 0
for i in range(int(m)):
    x, d = [float(i) for i in input().split()]
    if d < 0:
        avg += (d * mi) + x
    else:
        avg += (d * ma) + x

print(avg)