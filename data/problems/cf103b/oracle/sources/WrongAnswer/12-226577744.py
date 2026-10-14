import sys

input = sys.stdin.readline


############ ---- Input Functions ---- ############
def inp():
    return int(input())


def inlt():
    return list(map(int, input().split()))


def insr():
    s = input()
    return list(s[: len(s) - 1])


def invr():
    return map(int, input().split())


import collections

n, m = invr()
adj = [[] for _ in range(n)]
for i in range(m):
    a, b = invr()
    adj[a - 1].append(b - 1)
    adj[b - 1].append(a - 1)
dist = [-1 for _ in range(n)]
dist[0] = 0
count = [0]


def dfs(node, par):
    dist[node] = dist[par] + 1
    for nei in adj[node]:
        if nei != par:
            if dist[nei] != -1:
                count[0] = dist[node] - dist[nei]
                return True
            else:
                if dfs(nei, node):
                    return True
    return False


if not dfs(0, -1):
    print("NO")
    exit()
# print(dist, count)
if n == m and count[0] >= 2:
    print("FHTAGN!")
else:
    print("NO")