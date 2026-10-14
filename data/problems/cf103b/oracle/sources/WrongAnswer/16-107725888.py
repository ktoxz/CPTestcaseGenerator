from sys import stdin,stdout,setrecursionlimit
setrecursionlimit(10**4)
from collections import defaultdict
nmbr = lambda: int(stdin.readline())
lst = lambda: list(map(int,stdin.readline().split()))
def dfs(src,p1,p2):
    col[src]=1
    for neigh in g[src]:
        if neigh==p1 or neigh==p2:continue
        elif col[neigh]==0:
            if dfs(neigh,src,src)==False:
                return False
        elif col[neigh]==1:
            return False
    col[src]=2
    return True
for _ in range(1):#nmbr()):
    n,eg=lst();aa=bb=cc=-1
    g=defaultdict(set)
    for i in range(eg):
        u,v=lst()
        g[u].add(v)
        g[v].add(u)
    for a in range(1,n+1):
        for b in range(a+1,n+1):
            for c in range(b+1,n+1):
                if a in g[b] and b in g[c] and c in g[a]:
                    aa,bb,cc=a,b,c
                    break
    if aa==-1:
        print('NO')
        continue
    col=[0]*(1+n)
    if not dfs(aa,bb,cc):
        print('NO')
        continue
    col = [0] * (1 + n)
    if not dfs(bb, aa, cc):
        print('NO')
        continue
    col = [0] * (1 + n)
    if not dfs(cc, bb, aa):
        print('NO')
        continue
    print('FHTAGN!')