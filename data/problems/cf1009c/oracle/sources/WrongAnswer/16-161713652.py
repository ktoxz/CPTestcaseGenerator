n, m = map(int, input().split())
mean = 0
for i in range(m):
    x, d = map(int, input().split())
    mean = mean + x
    if d >= 0:
        mean = mean + (d * (n-1))/2
    else:
        if n % 2 == 1:
            mean = mean + (d * (n*n - 1))/4
        else: mean = mean + (d*n)/4
print(mean)