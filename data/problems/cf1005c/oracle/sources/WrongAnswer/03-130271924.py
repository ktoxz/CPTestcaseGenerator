a = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912]
n = int(input())
b = [int(i) for i in input().split()]
b.sort()
d = [False] * n
c = []
f = 0
for i in range(n):
    if b[i] == b[i-1]:
        d[i] = d[i-1]
        continue
    if d[i]:
        for j in range(i+1,n):
            if b[i] + b[j] in a:
                d[j] = True
        continue
    if b[i] in a:
        d[i] = True
        if b[i] not in c:
            c.append(b[i])
        else:
            c.remove(b[i])
    for j in range(i+1,n):
        if b[i] + b[j] in a:
            d[j] = True
            d[i] = True
f += len(c) + d.count(False)
print(f)


# Wed Sep 29 2021 16:52:52 GMT+0300 (Москва, стандартное время)