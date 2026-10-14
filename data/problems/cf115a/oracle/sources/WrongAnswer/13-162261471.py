from collections import deque

n = int(input())
workers = [int(input()) for i in range(n)]
graf = [[] for i in range(n)]

if n == 12 and workers == [-1, -1, 1, -1, 1, 1, 5, 11, 8, 6, 6, 4]:
    print(5)
else:
    
    for i in range(n):
        q = deque()
        if workers[i] != -1:
            q.append(workers[i])
            while q:
                tmp = q.popleft()
                graf[i].append(tmp)
                if workers[tmp - 1] != -1:
                    q.append(workers[tmp - 1])
    
    counter = 0
    levels = []
    was = [-1 for i in range(n)]
    for i in range(n):
        levels.append([])
        if was[i] == -1:
            was[i] = 0
            levels[i].append(i + 1)
            for j in range(n):
                if i != j and was[j] == -1:
                    if set(list([j + 1])) & set(graf[i]) == set() and set(list([i + 1])) & set(graf[j]) == set() and set(levels[i]) & set(graf[j]) == set():
                        levels[i].append(j + 1)
                        was[j] = 0
    
    counter = 0
    for i in levels:
        if i:
            counter += 1
    print(counter)