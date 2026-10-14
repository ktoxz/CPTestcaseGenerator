from collections import defaultdict, deque


g = defaultdict(list)

def bfs(init):
    v = [init]
    q = deque([init])

    while q:
        curr = q.popleft()

        for vec in g[curr]:
            if vec in v:
                continue
            v.append(vec)
            q.append(vec)

    return v


n, m = map(int, input().split())

for _ in range(m):
    i, j = map(int, input().split())
    g[i].append(j)
    g[j].append(i)

vis = bfs(1)

if n == m and len(vis) == len(g.keys()):
    print("FHTAGN!")
else:
    print("NO")