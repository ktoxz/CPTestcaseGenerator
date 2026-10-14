"""
    A ideia geral é modelar o problema como uma árvore, onde cada vértice é um empregado
    a arestas sao as relações de "chefia" entre os empregados. 

    Como os grupos só podem ser formados por empregados com mesmo nível de chefia, podemos considerar que um grupo agrupa 
    todos os empregados que estão no mesmo nível da árvore. Portanto, para sabermos o mínimo de grupos necessários, basta
    saber a altura da árvore e acrescir de 1, pois o vértice da raíz deve ser considerado. Vértices desconexos podem ser inclusos em quaisquer grupos.
"""

def dfs_max_height(graph, start):
    visited = set()
    stack = [(start, 0)]
    max_height = 0 # variable to store the maximum height found

    while stack:
        vertex, height = stack.pop()
        visited.add(vertex)
        max_height = max(max_height, height) # update the maximum height

        for neighbor in graph[vertex]:
            if neighbor not in visited:
                stack.append((neighbor, height + 1))

    return max_height

n = int(input())
graph = [[] for _ in range(0,n+1)]

for i in range(1, n+1):
    m = int(input())
    if m != -1:
        graph[m].append(i)


max = dfs_max_height(graph, 1)
print(max+1)