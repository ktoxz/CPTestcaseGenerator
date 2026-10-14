from collections import deque
n, m = map(int, input().split())
M = m
g = {i: [] for i in range(1, n + 1)}
while m:
    n1, n2 = map(int, input().split())
    g[n1].append(n2)
    g[n2].append(n1)
    m = m - 1
v = [False for _ in range(n + 1)]
cities = 0
for start in range(1, n + 1):
    if v[start] == False:
        v[start] = True
        queue = deque([start])
        while queue:
            curr = queue.popleft()
            for i in g[curr]:
                if v[i] == False:
                    v[i] = True
                    queue.append(i)
        cities = cities + 1
if M == n and cities == 1:
    print("FHTAGN!")
else:
    print('NO')