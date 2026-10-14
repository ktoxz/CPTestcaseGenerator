n, m = map(int, input().split())
p = [[0, 0, 0] for i in range(n + 1)]
for i in range(m):
    a, b, d = map(int, input().split())
    p[b][1], p[a][0], p[a][2] = a, b, d
for a in range(1, n + 1):
    if p[a][1] == 0:
        b, c, d = a, p[a][0], p[a][2]
        while c:
            if d > p[b][2]: d = p[b][2]
            b, c = c, p[c][0]
        print(a, b, d)