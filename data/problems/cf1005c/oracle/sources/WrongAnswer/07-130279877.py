a = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912]
n = int(input())
b = [int(i) for i in input().split()]
d = [False] * (max(b) + 1)
used = []
f = 0
for i in range(n):
    if d[b[i]] or b[i] in used:
        continue
    if b[i] in a:
        if b.count(b[i]) == 1:
            f += 1
        continue
    ok = True
    for j in range(29):
        if a[j] - b[i] in b:
            d[b[i]] = True
            d[a[j] - b[i]] = True
            ok = False
            break
    if ok:
        f += 1
        used.append(b[i])
print(f)



# Wed Sep 29 2021 18:15:22 GMT+0300 (Москва, стандартное время)