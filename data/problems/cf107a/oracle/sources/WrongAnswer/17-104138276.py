import math,sys,bisect,heapq
from collections import defaultdict,Counter,deque
from itertools import groupby,accumulate
#sys.setrecursionlimit(200000000)
int1 = lambda x: int(x) - 1
#def input(): return sys.stdin.readline().strip()
input = iter(sys.stdin.buffer.read().decode().splitlines()).__next__
ilele = lambda: map(int,input().split())
alele = lambda: list(map(int, input().split()))
ilelec = lambda: map(int1,input().split())
alelec = lambda: list(map(int1, input().split()))
def list2d(a, b, c): return [[c] * b for i in range(a)]
def list3d(a, b, c, d): return [[[d] * c for j in range(b)] for i in range(a)]
#MOD = 1000000000 + 7
def Y(c):  print(["NO","YES"][c])
def y(c):  print(["no","yes"][c])
def Yy(c):  print(["No","Yes"][c])
    
n,p = ilele()
G  = defaultdict(list)
P=  defaultdict(set)

def addEdge(a,b,c):
    G[a].append(b)
    G[b].append(a)
    P[a].add(c)
    P[b].add(c)

vis = [False]*(n+1)
  
def dfs(node):
    Ans = []
    vis[node] = True
    s = deque()
    mini = 1e9
    s.append(node)
    while s:
        x = s.pop()
        Ans.append(x)
        mini = min(mini,min(P[x]))
        for i in G.get(x,[]):
            if not vis[i]:
                s.append(i)
                vis[i]  = True
    return Ans,mini
                


tap = set()
tank = set()
for i in range(p):
    a,b,c = ilele()
    addEdge(a,b,c)
    tap.add(b)
    tank.add(a)

#print(tank,tap,G)
Ans2 = []
for i in range(1,n+1):
    if not vis[i]:
        Ans,mini = dfs(i)
        t1 = t2 = None
        for j in Ans:
            x = j in tap 
            y = j in tank
            if x^y:
                if x:
                    t1 = j
                else:
                    t2 = j
        if t1 and t2 and mini != None:
            Ans2.append((t2,t1,mini))
print(len(Ans2))
if Ans2:
    for i,j,k in Ans2:
        print(i,j,k)