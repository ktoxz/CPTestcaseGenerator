import collections
import sys


class Graph:
    def __init__(self, v: int):
        self.V = v
        self.graph = [[0 for col in range(self.V)]
                      for row in range(self.V)]

    def add_edge(self, u, v, weight):
        self.graph[u][v] = weight

    def is_tank(self, node):

        if len(list(filter(lambda x: x > 0, self.graph[node]))) == 0:
            return False

        for i in range(self.V):
            if i == node:
                continue
            if self.graph[i][node] > 0:
                return False

        return True

    def is_tap(self, node):
        if len(list(filter(lambda x: x > 0, self.graph[node]))) == 1:
            return False

        for i in range(self.V):
            if i == node:
                continue
            if self.graph[i][node] > 0:
                return True

        return False

    def get_all_tanks(self):
        tanks = []
        for i in range(self.V):
            if self.is_tank(i):
                tanks.append(i)

        return tanks

    def get_all_taps(self):
        taps = []
        for i in range(self.V):
            if self.is_tap(i):
                taps.append(i)

        return taps

    def min_diameter(self, source: int, dest: int):
        visited = [False] * self.V
        min_d = sys.maxsize

        return self.dfs_utill(visited, source, min_d, dest)

    def dfs_utill(self, visited, v, min_d, dest) -> int:
        visited[v] = True

        for neighbour in range(len(self.graph[v])):
            if not visited[neighbour]:
                if 0 < self.graph[v][neighbour] < min_d:
                    min_d = self.graph[v][neighbour]

                if neighbour == dest:
                    return min_d
                self.dfs_utill(visited, neighbour, min_d, dest)

        return -1


n, p = list(map(int, input().split()))
g = Graph(n)

for i in range(p):
    a, b, d = list(map(int, input().split()))
    g.add_edge(a - 1, b - 1, d)

tanks = g.get_all_tanks()
taps = g.get_all_taps()

free_taps = [True] * g.V

for i in tanks:
    for j in taps:
        if not free_taps[j]:
            continue
        if g.min_diameter(i, j) > -1:
            free_taps[j] = False
            print(i + 1, j + 1, g.min_diameter(i, j))
            break