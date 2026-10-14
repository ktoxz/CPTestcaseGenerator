import math

n, p = map(int, input().split())
neighList = [() for _ in range(n)]
in_degrees = [0] * n
for _ in range(p):
  a, b, d = map(int, input().split())
  a -= 1; b-= 1
  neighList[a] = (b, d)
  in_degrees[b] += 1

def dfs(u, d):
  if len(neighList[u]) == 0:
    return (u, d)
  else:
    return dfs(neighList[u][0], min(d, neighList[u][1]))
    
res = []
for u in range(n):
  if in_degrees[u] == 0:
    b, d = dfs(u, math.inf)
    res.append((u+1, b+1, d))
    
res.sort()
print(len(res))
for r in res:
  print(*r)