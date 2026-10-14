import sys,os
 
if os.path.exists('input.txt'):
    sys.stdin = open('input.txt', 'r')
    sys.stdout = open('output.txt', 'w')


from collections import deque, defaultdict

def solve(graph, start):
    dq = deque()
    dq.append(start)
    steps = 0

    while dq:
        for i in range(len(dq)):
            u = dq.popleft()
            for v in graph[u]:
                dq.append(v)

        steps += 1

    return steps 

def main():
    n = int(sys.stdin.readline().strip())
    arr = []
    graph = defaultdict(list)
    for i in range(n):
        x = int(sys.stdin.readline().strip())
        arr.append(x)
        if x != -1:    
            graph[x].append(i+1)

    depth = 0
    for i in range(1, n+1):
        if arr[i-1] == -1:
            depth = max(depth, solve(graph, i))

    print(depth)


main()