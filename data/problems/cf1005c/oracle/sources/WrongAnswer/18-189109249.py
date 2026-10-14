n = int(input())
s = list(map(int, input().split()))
d = {}
for i in range(n):
    d[s[i]] = 1
a = []
w = 0
for i in range(1, 31):
    a.append(2 ** i)
for i in range(n):
    f = 0
    if s[i] in a:
        if s.count(s[i]) == 1:
            w = w + 1
            continue
    for j in range(30):
        if a[j] - s[i] in d:
            f = 1
            break
    if f == 0:
        w = w + 1

print(w)