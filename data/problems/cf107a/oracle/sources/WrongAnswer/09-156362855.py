def dfs(g, s, mn):
    if g.get(s, -1) == -1:
        return s, mn
    if sizes[s] < mn or mn == -1:
        mn = sizes[s]
    return dfs(g, g[s], mn)


n, p = map(int, input().split())

in_links = dict()
links = dict()
sizes = dict()
for i in range(n):
    in_links[i + 1] = -1
for i in range(p):
    a, b, d = map(int, input().split())
    in_links[b] = a
    links[a] = b
    if a not in sizes or d < sizes[a]:
        sizes[a] = d
    if b not in sizes or d < sizes[b]:
        sizes[b] = d

res = []
for k, v in in_links.items():
    if v == -1:
        a, b = dfs(links, k, -1)
        res.append((k, a, b, ))
print(len(res))
print('\n'.join([' '.join(map(str, tup)) for tup in res]))