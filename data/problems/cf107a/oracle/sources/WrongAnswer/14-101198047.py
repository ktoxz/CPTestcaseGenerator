from sys import stdin, stdout

def find(node):
    x = []
    while dsu[node] > 0:
        x.append(node)
        node = dsu[node]
    for i in x:
        dsu[i] = node
    return node

def union(node1, node2):
    p1 = find(node1)
    p2 = find(node2)
    if p1 != p2:
        pair = (o_c[p1][0], o_c[p2][1])
        if dsu[p1] > dsu[p2]:
            p1, p2 = p2, p1
        dsu[p1] += dsu[p2]
        minm[p1] = min(minm[p1],minm[p2])
        dsu[p2] = p1
        o_c[p1] = pair
    else:
        cycle[p1] = False

n, m = map(int, stdin.readline().strip().split())
dsu = [-1]*(n+1)
cycle = [True]*(n+1)
o_c = [(i,i) for i in range(n+1)]
minm = [float('inf')]*(n+1)
freq = [0]*(n+1)
for __ in range(m):
    a, b, c = map(int, stdin.readline().strip().split())
    freq[a] += 1
    freq[b] += 1
    union(a, b)
    minm[a] = min(minm[a], c)
    minm[b] = min(minm[b], c)
output = []
for i in range(1, n+1):
    if dsu[i]<0 and cycle[i]:
        output.append((o_c[i][0],o_c[i][1], minm[i]))
output = sorted(output, key = lambda t: t[0])
if not output:
    print(0)
else:
    print(len(output))
    for out in output:
        print(*out)