class Graph():
    def __init__(self, number_nodes):
        self.nodes = [0] * (number_nodes+1)
        for i in range(number_nodes):
            self.nodes[i+1] = Node(i+1)
        
    def connect(self, node_1, node_2):
        self.find(node_1).neighbors.append(self.find(node_2))
        self.find(node_2).neighbors.append(self.find(node_1))
    
    def find(self, i):
        return self.nodes[i]

    def bfs(self):
        stack = []
        stack.append(self.nodes[1])
        visited = {}
        while(stack):
            current = stack.pop()
            visited[current.value] = 1
            for neighbor in current.neighbors:
                if neighbor.value not in visited:
                    neighbor.known_by = current
                    stack.append(neighbor)
                else:
                    if current.known_by != neighbor:
                        return("FHTAGN!")
        return("NO")    

class Node():
    def __init__(self, value):
        self.value = value
        self.neighbors = []
        self.known_by = self
        
vertices, edges = [int(s) for s in input().split()]
graph = Graph(vertices)
for i in range(edges):
    node_1, node_2 = [int(s) for s in input().split()]
    graph.connect(node_1, node_2)

print(graph.bfs())