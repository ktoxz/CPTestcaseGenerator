a = int(input())
b = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576,
     2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912]
c = {}
d = 0
y = 0
f = []
s = list(map(int, input().split()))
for i in range(a):
    for j in range(len(b)):
        f.append(b[j] - s[i])
    c[s[i]] = f
    f = []
for i in range(a):
    for j in range(len(b)):
        if c[s[i]][j] in s:
            y = 1
    if not y and s[i] in b and s.count(s[i]) == 1:
        d += 1
    y = 0
print(d)