from collections import defaultdict

nodos=defaultdict(list)
n,m=map(int,input().split(' '))
for i in range(m):
  a,b=map(int,input().split(' '))
  nodos[a-1].append(b-1)
  nodos[b-1].append(a-1)

visitadas=[False]*n

def DFS(nodo):
  visitadas[nodo]=True
  for i in nodos[nodo]:
    if not visitadas[i]:
      DFS(i)

conjuntos=0

for i in nodos.keys():
  if not visitadas[i]:
    DFS(i)
    conjuntos+=1
if conjuntos==1 and n==m: print('FHTAGN!')
else: print('NO')