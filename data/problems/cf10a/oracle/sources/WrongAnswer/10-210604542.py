n, p1, p2, p3, t1, t2 = map(int, input().split())
l = []
for _ in range(n):
    l.append(list(map(int, input().split())))
ans = 0
for i in range(n):
    x = l[i][0]
    y = l[i][1]
    ans += (y - x) * p1
for i in range(n-1):
    z = l[i+1][0] - l[i][1]
    if z <= t1:
        ans += p1 * z
    elif t1 < z <= t2:
        ans += p1 * t1 + p2 * (z - t1)
    elif z > t2:
        ans += p1 * t1 + p2 * t2 + p3 * (z - t2 - t1)
print(ans)