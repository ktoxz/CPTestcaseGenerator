import heapq;
import math;
from collections import deque, Counter;
import sys;

mod = 998244353;
input = sys.stdin.readline;





n, p = map(int, input().split())


inDegree = [0 for node in range(n)]


neighbourNodes = [[] for i in range(n)]

for i in range(p):
    path, toPath, di = map(int, input().split())

    neighbourNodes[path - 1].append([toPath - 1, di])
    inDegree[toPath - 1] += 1;



res = []

visited = [0 for node in range(n)]

def bfs(node):
    queue = deque([[node, float('inf')]]);

    lastNode, mnFlow = None, float('inf');
    while(queue):
        currNode, maxFlow = queue.popleft()
        lastNode = currNode;
        mnFlow = maxFlow
        visited[currNode] = 1;
        for node, cs in neighbourNodes[currNode]:
            if visited[node]: continue;
            maxFlow = min(maxFlow, cs);
            queue.append([node, maxFlow])
    return lastNode, mnFlow;


for node in range(n):
    if not inDegree[node]:
        lastNode, cs = bfs(node)
        if lastNode != node:
            res.append([node + 1, lastNode + 1, cs])

res.sort()


print(len(res))

for nodeOne, nodeTwo, cs in res:
    print(nodeOne, nodeTwo, cs);