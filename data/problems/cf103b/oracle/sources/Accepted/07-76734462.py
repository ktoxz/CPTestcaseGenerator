#!/usr/bin/env python3

n, m = map(int, input().rstrip().split())
adj = [[] for i in range(n+1)]
vis = [False for i in range(n+1)]

for i in range(m):
    u, v = map(int, input().rstrip().split())
    adj[u].append(v)
    adj[v].append(u)


def dfs(cur):
    cnt = 1
    vis[cur] = True
    for nxt in adj[cur]:
        if not vis[nxt]:
            cnt += dfs(nxt)

    return cnt


if n != m or dfs(1) != n:
    print("NO")
else:
    print("FHTAGN!")