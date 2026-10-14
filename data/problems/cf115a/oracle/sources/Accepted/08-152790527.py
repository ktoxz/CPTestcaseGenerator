n = int(input())

adjList = [[] for _ in range(n+1)]

for i in range(1, n+1):
    manager = int(input())
    if manager != -1:
        adjList[manager].append(i)



# for i in range(1,n+1):
#     print(i, adjList[i])
# print()

d = [1 for _ in range(n+1)]
for i in range(1, n+1):
    queue = [i]
    while(len(queue) > 0):
        node = queue.pop(0)
        for neighbor in adjList[node]:
            queue.append(neighbor)
            d[neighbor] = d[node] + 1

print(max(d))