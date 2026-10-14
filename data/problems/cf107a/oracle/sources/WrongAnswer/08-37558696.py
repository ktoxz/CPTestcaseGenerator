import math
n,p = map(int, input().split())
g = [[-1,-1] for _ in range(n+1)]
t = set(range(1, n+1))
for i in range(p):
    a,b,d =map(int, input().split())
    g[a] = [b, d]
    t.remove(b)
ans = []
for tt in t:
    c = g[tt][0]
    m = g[tt][1]
    while g[c][0] != -1:
        m = min(m, g[c][1])
        c = g[c][0]
    if m > -1:
        ans.append('%i %i %i' % (tt,c,m))
if len(ans) == 0:
    print(0)
else:
    print('\n'.join(ans))