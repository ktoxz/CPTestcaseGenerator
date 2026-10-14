import sys
input = sys.stdin.readline

n, p = map(int, input().split())
d = [0]*(n+1)
d1 = d.copy()
d2 = d.copy()
for i in range(p):
    a, b, c = map(int, input().split())
    d[b] = a
    d1[a] = b
    d2[a] = c

ans = []
for i in range(1, n+1):
    if d[i]:
        continue

    x = i
    y = d2[x]
    while d1[x]:
        y = min(y, d2[x])
        x = d1[x]
    if y:
        ans.append([i, x, y])
print(len(ans))
for i in ans:
    print(' '.join(map(str, i)))