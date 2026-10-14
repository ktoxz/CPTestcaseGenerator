import sys 
from collections import defaultdict
input = sys.stdin.readline 

def parent(v, p):
    if(p[v] == v):
        return v 
    return parent(p[v], p) 
    
def union(p, x, y):
    p[x] = y

n, m = map(int, input().split()) 
d = defaultdict(list) 

for i in range(m):
    u, v = map(int, input().split()) 
    d[u].append(v) 
    
p = [i for i in range(n + 1)]
c = 0
for i in d.keys():
    for j in d[i]:
        x = parent(i, p) 
        y = parent(j, p) 
        if(x == y):
            c += 1 
        else:
            union(p, x, y) 
if(c == 1):
    print("FHTAGN!") 
else:
    print("NO")