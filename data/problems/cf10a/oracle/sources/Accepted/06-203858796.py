n, p1, p2, p3, t1, t2 = (int(i) for i in input().split())
res = pr = 0
for _ in range(n):
    l, r = (int(i) for i in input().split())
    res += (r - l) * p1
    pr = pr if pr > 0 else l
    idle = min(t1, max(0, l - pr))
    res += idle * p1
    screensaver = min(t2, max(0, l - pr - idle))
    res += screensaver * p2
    res += max(0, l - pr - idle - screensaver) * p3
    pr = r
print(res)