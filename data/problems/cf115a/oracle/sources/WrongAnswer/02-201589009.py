class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return str(self.data)
    
    def __str__(self):
        return self.__repr__()

class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, elem):
        if self.head:
            # inserção quando a lista já possui elementos
            pointer = self.head
            while pointer.next:
                pointer = pointer.next
            pointer.next = Node(elem)
        else:
            # primeira inserção
            self.head = Node(elem)
        self._size += 1

    def _getNode(self, index):
        pointer = self.head
        for i in range(index):
            if pointer:
                pointer = pointer.next
            else:
                raise IndexError("list index out of range")
        return pointer

    def __len__(self): 
            # retorna o tamanho da lista
            return self._size
        
    def __getitem__(self, index):
            # a = lista[x]
        pointer = self._getNode(index)
        if pointer:
            return pointer.data
        raise IndexError("list index out of range")

    def __setitem__(self, index, elem):
        # lista[x] = a
        pointer = self._getNode(index)
        if pointer:
            pointer.data = elem
        else:
            raise IndexError("list index out of range")
        
        
    def index(self, elem):
        # retorna o índice de elem na lista
        pointer = self.head
        i = 0
        while(pointer):
            if pointer.data == elem:
                return i
            pointer = pointer.next
            i += 1
        return -1
    
    def insert(self, index, elem):
        # insere elem na posição index
        node = Node(elem)
        if index == 0:
            node.next = self.head
            self.head = node
        else:
            pointer = self._getNode(index-1)
            node.next = pointer.next
            pointer.next = node
        self._size += 1

    def remove(self, elem):
        # remove elem da lista
        if self.head == None:
            raise ValueError("{} is not in list".format(elem))
        elif self.head.data == elem:
            self.head = self.head.next
            self._size -= 1
            return True
        else:
            ancestor = self.head
            pointer = self.head.next
            while pointer:
                if pointer.data == elem:
                    ancestor.next = pointer.next
                    pointer.next = None
                    self._size -= 1
                    return True
                ancestor = pointer
                pointer = pointer.next
            raise ValueError("{} is not in list".format(elem))
        
    def __repr__(self):
        if self.head == None:
            return ""
        r = str(self.head.data)
        pointer = self.head.next
        while pointer:
            r += " -> " + str(pointer.data)
            pointer = pointer.next
        return r

    def __str__(self):
        return self.__repr__()
    
class Graph:
    def __init__(self, n):
        self.vertexList = []
        self.edges = 0
        self.vertices = 0
        self.current = 1

        for _ in range(n):
            self.addVertex()

    def getVertex(self, u):
        return self.vertexList[u-1]

    def addVertex(self):
        new_vertex = LinkedList()
        # new_vertex.append(self.current)
        self.vertexList.append(new_vertex)
        self.current += 1
        self.vertices += 1
    
    def _addEdgeAux(self, u, v):
        # currentVertex = self._getVertex(v)
        currentVertex = self.getVertex(u)
        currentVertex.append(v)

    def addEdge(self, u, v):
        self._addEdgeAux(u, v)
        # self._addEdgeAux(v, u)
        self.edges += 1

    def __repr__(self):
        if self.vertices <= 0:
            return ""
        else:
            r = '1: ' + str(self.vertexList[0])
            for i in range(1,self.vertices):
                r += f'\n{str(i+1)}: {str(self.vertexList[i])}'
            return r
    
    def __str__(self):
        return self.__repr__()

n = int(input())
T = Graph(n)

for i in range(1, n+1):
    parent = int(input())
    if parent != -1:
        T.addEdge(parent, i)

maxLevel = 1

def dfs(G, v, max_level):
    ml = max_level
    adj = G.getVertex(v)
    if len(adj) == 0:
        return 1
    else:
        for w in adj:
            x = dfs(G, w, ml)
            ml = max(ml, x+1)
        return ml
        
print(dfs(T, 1, 1))

# print(T)