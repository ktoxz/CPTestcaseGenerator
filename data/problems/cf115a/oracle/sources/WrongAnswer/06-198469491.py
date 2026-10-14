n = int(input())
v_list = list()
for i in range(n):
    v_list.append(int(input()))
    
def create_graph(v_list):
    graph = [[0] * len(v_list) for v in v_list]
    for i in range(len(v_list)):
        if v_list[i] != -1:
            graph[i][v_list[i]-1] = 1
            graph[v_list[i]-1][i] = 1
    return graph

graph = create_graph(v_list)

visited = [False] * n
prev_list = [None] * n
groups = list()

def check_employer(v, prev_list, groups):
    if len(groups) == 0:
        groups.append([v])
    else:
        for group in groups:
            flag = False
            prev = prev_list[v]
            while prev is not None:
                if prev in group:
                    flag = True
                    break
                prev = prev_list[prev]
            if not flag:
                group.append(v)
                return    
        groups.append([v])

def dfs(start, prev, prev_list, visited, graph):
    visited[start] = True
    prev_list[start] = prev
    check_employer(start, prev_list, groups)
    for i in range(len(graph[start])):
        if graph[start][i] != 0 and not visited[i]:
            dfs(i, start, prev_list, visited, graph)
            
for i in range(len(visited)):
    if not visited[i]:
        dfs(i, None, prev_list, visited, graph)
        
print(len(groups))