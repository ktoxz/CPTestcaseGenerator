from collections import defaultdict, deque
from functools import lru_cache
import threading
from sys import stdin,stdout,setrecursionlimit

def inp():
    return stdin.readline()

def inpnum():
    return int(stdin.readline())

def inpli():
    return list(map(int, stdin.readline().strip().split()))

def inpst():
    s = stdin.readline().strip()
    return list(s[:len(s)])

def inpnums():
    return map(int, stdin.readline().strip().split())

def main():
    
    n = inpnum()

    # build graph
    graph = defaultdict(list)
    for node in range(1, n + 1):
        parent = inpnum()
        graph[parent].append(node)
    
    def bfs(node):
        deepth = 0
        queue = deque([node, deepth])
        visited = set()

        while queue:
            n = len(queue)
            deepth += 1

            for _ in range(n):

                root = queue.popleft()
                visited.add(root)

                for nei in graph[root]:
                    if nei not in visited:
                        queue.append(nei)
        return deepth

    result = 0
    roots = graph[-1]
    
    for root in roots:
        result = max(result, bfs(root))
    
    print(result)

main()