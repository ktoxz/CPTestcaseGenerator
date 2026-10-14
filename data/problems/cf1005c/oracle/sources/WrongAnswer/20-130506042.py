n = int(input())
nl = list(map(int, input().split()))
a = []
for i in range(1, 31):
    a.append(2**i) 
k = 0
c = 0
s = 0
for i in nl:
    if nl.count(i) >= 2:
        s += 1


for i in nl:
    for j in nl:
        if ((i+j) in a) and (i != j) and (c == 0):
            k += 1
            c += 1
    c = 0

if n - k == 0:
    print(0)
else:
    print(n - k - s)
# Fri Oct 01 2021 23:55:33 GMT+0300 (Москва, стандартное время)