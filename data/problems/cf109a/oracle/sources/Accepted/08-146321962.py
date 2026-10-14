n = int(input())

flag = False
idx = (-1, -1)
for i in range(0, n):
    for j in range(0, n):
        if 4 * i + 7 * j > n:
            break
        if 4 * i + 7 * j == n:
            idx = (i, j)
            flag = True
            break
    if flag:
        break

if idx == (-1, -1):
    print(-1)
else:
    print('4' * idx[0] + '7' * idx[1])