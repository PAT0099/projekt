class Graph:
    """
    Main class that holds a graph and all its vertices
    """

    class Vertex:
        """
        Vertex class, holds information about a single vertex
        """
        def __init__(self):
            """
            Initialize vertex
            """
            # dictionary of form neighbor: edge_weight
            self._neighbors: dict = {}
            # state for algorithms to use
            self._state: int = 0
            # for rendering
            self._loc_x: float = 0
            self._loc_y: float = 0

        def __str__(self) -> str:
            return f"{self._state}, {self._neighbors.__str__()}"
        
        def __repr__(self) -> str:
            return self.__str__()
        
        @property
        def _neighbor_count(self):
            return len(self._neighbors)
        
        def move_vertex(self, x: float, y: float):
            """
            Change location of vertex
            """
            self._loc_x = x
            self._loc_y = y
        
        def set_edge(self, to_vertex: int, weight: float = 1):
            """
            Change value of edge going to another vertex
            """
            self._neighbors[to_vertex] = weight

        def remove_edge(self, to_vertex: int):
            """
            Remove an edge going to another vertex
            """
            if to_vertex in self._neighbors:
                self._neighbors.pop(to_vertex)

    def __init__(self):
        """
        Initialize graph
        """
        self._vertices: list(Graph.Vertex) = []

    def __str__(self) -> str:
        ret = "Graph:\n"
        for i in range(len(self._vertices)):
            ret += f"{i:>4} - {self._vertices[i].__str__()}\n"
        return ret

    def __repr__(self) -> str:
        return self.__str__()
    
    @property
    def _vertex_count(self):
        return len(self._vertices)

    def wrong_index(self, index: int) -> bool:
        """
        Returns True if desired index is invalid
        """
        if index < 0 or index >= len(self._vertices) or type(index) != int:
            return True
        return False
    
    def at(self, index: int) -> Vertex:
        """
        Points to vertex at location `index`
        """
        if self.wrong_index(index):
            return None
        return self._vertices[index]
    
    def set_connection(self, from_vertex: int, to_vertex: int, value: float = 1, bidirectional: bool = False):
        """
        Set an edge between two vertices
        """
        if self.wrong_index(from_vertex):
            print("Invalid FROM index")
            return
        elif self.wrong_index(to_vertex):
            print("Invalid TO vertex")
            return
        
        self._vertices[from_vertex].set_edge(to_vertex, value)
        if bidirectional:
            self._vertices[to_vertex].set_edge(from_vertex, value)

    def remove_connection(self, from_vertex: int, to_vertex: int, bidirectional: bool = False):
        """
        Remove an edge between two vertices
        """
        if self.wrong_index(from_vertex):
            print("Invalid FROM index")
            return
        elif self.wrong_index(to_vertex):
            print("Invalid TO vertex")
            return
        
        self._vertices[from_vertex].remove_edge(to_vertex)
        if bidirectional:
            self._vertices[to_vertex].remove_edge(from_vertex)

    def add_vertex(self, loc_x: float = 0, loc_y: float = 0):
        """
        Add a single vertex
        """
        v = Graph.Vertex()
        v.move_vertex(loc_x, loc_y)
        self._vertices.append(v)

    def remove_vertex(self, index: int):
        """
        Remove a vertex
        """
        if self.wrong_index(index):
            print("Invalid index")
            return
        
        for v in self._vertices:
            v.remove_edge(index)
            v._neighbors = dict((neighbor if neighbor < index else neighbor-1, v._neighbors[neighbor]) for neighbor in v._neighbors)

        self._vertices.pop(index)

    def move_vertex(self, index: int, new_x: float = 0, new_y: float = 0):
        """
        Move vertex for graphical output
        """
        if self.wrong_index(index):
            print("Invalid index")
            return
        self._vertices[index].move_vertex(new_x, new_y)

    def reset_vertex_states(self, state = 0):
        """
        Resets state of all vertices
        """
        for v in self._vertices:
            v._state = state

    def reset_graph(self):
        """
        Removes all vertices
        """
        self._vertices = []

    def load_file(self, filename: str):
        """
        Load graph from a file given by parameter `filename`
        """
        lines = ""
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
        except FileNotFoundError:
            print("File not found")
        finally:
            datamode = 0
            for l in lines:
                if len(l) == 1:
                    continue
                elif l[0] == '#':
                    continue
                elif l[0] == 'v':
                    datamode = 1 #reading vertices
                    continue
                elif l[0] == 'e':
                    datamode = 2 #reading edges
                    continue
                
                if datamode == 1:
                    vert = l.strip().split(' ')
                    if len(vert) != 2:
                        print("Invalid input")
                        self.reset_graph()
                        return
                    self.add_vertex(float(vert[0]), float(vert[1]))
                    
                elif datamode == 2:
                    edge = l.strip().split(' ')
                    if len(edge) != 3:
                        print("Invalid input")
                        self.reset_graph()
                        return
                    self.set_connection(int(edge[0]), int(edge[1]), float(edge[2]))
           
    def save_file(self, filename: str):
        """
        Save graph into a file given by parameter `filename`
        """
        try:
            with open(filename, 'w') as f:
                f.write("# File generated by GraphManager\n\nv\n")
                for v in self._vertices:
                    f.write(f"{v._loc_x} {v._loc_y}\n")
                f.write("\ne\n")
                for v in range(self._vertex_count):
                    for e in self.at(v)._neighbors.keys():
                        f.write(f"{v} {e} {self.at(v)._neighbors[e]}\n")
        except Exception:
            print("Something went wrong")