def skuchno(mn, q, i, v):
    p = q[i]
    if p[1] < mn:
        mn = p[1]
    if p[0] in v:
        return p[0], mn
    return skuchno(mn, q, p[0], v)
n, m = map(int, input().split())
q = {}
v = set()
iz = set()
for _ in range(m):
    a, c, d = map(int, input().split())
    q[a] = [c, d]
    v.add(c)
    iz.add(a)
v, iz = v - iz, iz - v
print(len(iz))
for i in iz:
    g, k = skuchno(10 ** 12, q, i, v)
    print(i, g, k)