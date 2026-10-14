import sys
import queue
sys.setrecursionlimit(100000)

# global constant
INF = int(1e7+1)
MAX = 100005

# For testing
#sys.stdin = open("INP.txt", 'r')
#sys.stdout = open("OUT.txt", 'w')

# global variables
parents = []
ranks = []
size = []
n = 0

# classes


class Pair:
    def __init__(self, a, b):
        self.first = a
        self.second = b


# functions
def init():
    global parents, ranks, size
    parents = [i for i in range(n)]
    ranks = [0 for i in range(n)]
    size = [1 for i in range(n)]


def findSet(u):
    if(parents[u] != u):
        parents[u] = findSet(parents[u])
    return parents[u]


def unionSet(u, v):
    up = findSet(u)
    vp = findSet(v)
    if up == vp:
        return
    if ranks[up] < ranks[vp]:
        parents[up] = vp
    elif ranks[vp] < ranks[up]:
        parents[vp] = up
    else:
        ranks[vp] += 1
        parents[up] = vp


# main function
def main():
    global n
    n, m = map(int, input().split())
    init()
    flag = False
    firstLoop = False
    for i in range(m):
        u, v = map(int, input().split())
        u -= 1
        v -= 1
        if findSet(u) == findSet(v):
            flag = True
            if not firstLoop:
                firstLoop = True
            else:
                flag = False
                break
        unionSet(u, v)
    S = set()
    if flag:
        for i in range(n):
            S.add(findSet(i))
    if flag and len(S) > 1:
        flag = False
    if flag:
        print("FHTAGN!")
    else:
        print("NO")


main()