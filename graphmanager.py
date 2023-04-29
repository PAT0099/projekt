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
            return f"state {self._state}, {self._neighbors.__str__()}"
        
        def __repr__(self) -> str:
            return self.__str__()
        
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
    
    def _wrong_index(self, index: int) -> bool:
        """
        Returns True if desired index is invalid
        """
        if index < 0 or index >= len(self._vertices) or type(index) != int:
            return True
        return False
    
    def _at(self, index: int) -> Vertex:
        """
        Points to vertex at location `index`
        """
        if self._wrong_index(index):
            return None
        return self._vertices[index]
    
    def set_connection(self, from_vertex: int, to_vertex: int, value: float = 1, bidirectional: bool = False):
        """
        Set an edge between two vertices
        """
        if self._wrong_index(from_vertex):
            print("Invalid FROM index")
            return
        elif self._wrong_index(to_vertex):
            print("Invalid TO vertex")
            return
        
        self._vertices[from_vertex].set_edge(to_vertex, value)
        if bidirectional:
            self._vertices[to_vertex].set_edge(from_vertex, value)

    def remove_connection(self, from_vertex: int, to_vertex: int, bidirectional: bool = False):
        """
        Remove an edge between two vertices
        """
        if self._wrong_index(from_vertex):
            print("Invalid FROM index")
            return
        elif self._wrong_index(to_vertex):
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
        if self._wrong_index(index):
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
        if self._wrong_index(index):
            print("Invalid index")
            return
        self._vertices[index].move_vertex(new_x, new_y)

    def reset_vertex_states(self):
        """
        Resets state of all vertices to 0
        """
        for v in self._vertices:
            v._state = 0

    def load_file(self, filename: str):
        """
        Load graph from a file given by parameter `filename`
        """
        pass

    def save_file(self, filename: str):
        """
        Save graph into a file given by parameter `filename`
        """
        pass