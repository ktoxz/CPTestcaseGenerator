class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return self.data
    
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
    def __init__(self):
        self.vertexList = []
        self.edges = 0
        self.vertices = 0

    def _getVertex(self, u):
        currentVertex = None
        i = 0
        while i < self.vertices and currentVertex == None:
            if self.vertexList[i][0].data == u:
                currentVertex = self.vertexList[i]
            i += 1
        if currentVertex == None:
            raise ValueError("Vértice inválido!")  
        return currentVertex

    def insertVertex(self, name):
        new_vertex = LinkedList()
        new_vertex.append(Node(name))
        for i in range(self.vertices):
            if self.vertexList[i][0].data == name:
                raise ValueError("O vértice {} já existe no grafo!".format(name))
        self.vertexList.append(new_vertex)
        self.vertices += 1

    def removeVertex(self, name):
        find = 0
        i = 0
        j = 0
        while i < self.vertices and find == 0:
            if self.vertexList[i][0].data == name:
                self.vertexList.pop(i)
                self.vertices -= 1
                find = 1
            i += 1
        if find == 0:
            raise ValueError("O vértice {} não se encontra no grafo!".format(name))
        for i in range(self.vertices):
            if self.vertexList[i].index(name) != -1:
                self.vertexList[i].remove(name)
    
    def _insertEdgeAux(self, u, v):
        currentVertex = self._getVertex(v)
        currentVertex = self._getVertex(u)
        currentVertex.append(v)

    def insertEdge(self, u, v):
        self._insertEdgeAux(u, v)
        # self._insertEdgeAux(v, u)
        self.edges += 1
    
    def _removeEdgeAux(self, u, v):
        currentVertex = self._getVertex(u)
        currentVertex.remove(v)
        
    def removeEdge(self, u, v):
        self._removeEdgeAux(u, v)
        # self._removeEdgeAux(v, u)
        self.edges -= 1

    def connected(self, u, v):
        vertex = self._getVertex(u)
        if vertex.index(v) != -1:
            return True
        return False
    
    def degree(self, u):
        vertex = self._getVertex(u)
        return len(vertex) - 1

    def __repr__(self):
        if self.vertices <= 0:
            return ""
        else:
            r = str(self.vertexList[0])
            for i in range(1,self.vertices):
                r += "\n" + str(self.vertexList[i])
            return r
    
    def __str__(self):
        return self.__repr__()

if __name__ == '__main__':
    G = Graph()

    n = int(input())
    roots = []
    levels = []

    for i in range(n):
        G.insertVertex(str(i))

    for i in range(n):
        v = int(input())
        if v == -1:
            roots.append(str(i))
        else:
            G.insertEdge(str(v-1), str(i))

    def level_of(root):
        v = G._getVertex(root)
        return len(v)

    for i in roots:
        levels.append(level_of(i))

    max_level = max(levels)
    print(max_level)