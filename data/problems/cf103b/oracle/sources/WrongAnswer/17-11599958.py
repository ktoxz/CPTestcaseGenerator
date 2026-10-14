def dfs(graph, start):
    visited[start] = True
    for i in graph[start]:
        if not visited[i]:
            dfs(graph, i)

a, b = list(map(int, input().split(' ')))
g = {}
for i in range(1, a+1):
    g[i] = []


for i in range(b):
    x, y = map(int, input().split(' '))
    g[x].append(y)
    g[y].append(x)

visited = [True] + [False] * a

dfs(g, 1)
if False in visited:
    print("NO")

if a != b:
    print("NO")

    print("FHTAGN!")