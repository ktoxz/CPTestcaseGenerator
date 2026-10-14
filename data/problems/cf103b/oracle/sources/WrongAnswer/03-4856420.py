class Node:
    def __init__(self, n_name):
        """
        String, list of edges -> node
        """
        self.name = n_name
        self.edges = []
        self.incoming_edges = []

    def __str__(self):
        string = 'Name : ' + str(self.name) + ' \n'
        string += 'outcoming edges : ' + '\n'
        for edge in self.edges:
            string += str(edge) + '\n'
        return string
        

    def add_edge(self, edge):
        """
        edge -> None
        """
        self.edges.append(edge)

class Edge:
    def __init__(self, e_source, e_destination, weight = 1):
        """
        Node, Node, number -> Edge
        """
        self.source = e_source
        self.destination = e_destination
        self.weight = weight

    def __str__(self):
        string = 'source : ' + str(self.source.name) + ' \n'
        string += 'destination : ' + str(self.destination.name) + ' \n'
        string += 'weight : ' + str(self.weight) + '\n'
        return string

    def __lt__(self, other):
        return self.weight < other.weight

class Graph:
    def __init__(self):
        self.node_list = []
        self.edge_list = []
        self.name_to_node = {}

    def __str__(self):
        output = ""
        output += "Nodes : "
        for node in self.node_list:
            output += str(node.name)  + "  "
        output += "\nEdges : "
        for edge in self.edge_list:
            output += str(edge.source.name) + "--(" + str(edge.weight) + ")--" + str(edge.destination.name) + "  "
        output += "\n"
        return output

    def add_node(self, node_name):
        """
        (String or integer) -> Node
        Adds a node to the graph
        """
        new_node = Node(node_name)
        
        self.node_list += [new_node]
        self.name_to_node[node_name] = new_node
        
        return new_node

    def add_edge(self, source_name, dest_name, weight = 1):
        """
        (String or number), (String or number) -> (Edge)
        Adds an edge between two nodes
        if the nodes are not there it will create then
        """
        if source_name not in self.name_to_node :
            self.add_node(source_name)

        if dest_name not in self.name_to_node :
            self.add_node(dest_name)

        source_node = self.name_to_node[source_name]
        dest_node = self.name_to_node[dest_name]
        new_edge = Edge(source_node, dest_node, weight)
        
        
        source_node.add_edge(new_edge)
        dest_node.incoming_edges += [new_edge]
        self.edge_list += [new_edge]


def get_cycles(source, level, levels, cycles):
    # Mark source as explored
    levels[source] = level

    # DFS throught all of its neibour
    for edge in source.edges:
        next_vertex = edge.destination

        # If it's not explored then DFs it else then it's a cycle
        if next_vertex not in levels:
            get_cycles(next_vertex, levels[source] + 1, levels, cycles)
        else:
            cycle_length = levels[next_vertex] - levels[source] + 1
            if abs(cycle_length) > 2:                
                cycles.append(abs(cycle_length))

def is_Cthulhu(cycles):
    return len(cycles) == 1 and cycles[0] >= 3

# Construct a graph
a = Graph()
first_line = input()
first_line = first_line.split()
n = int(first_line[0])
m = int(first_line[1])

for i in range(m):
    line = input()
    line = line.split()
    s = int(line[0])
    t = int(line[1])
    a.add_edge(s, t)
    a.add_edge(t, s)
cycles = []
get_cycles(a.name_to_node[1], 0, {}, cycles)
if is_Cthulhu(cycles):
    print("FHTAGN!")
else:
    print("NO")