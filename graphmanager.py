# space for imports
import numpy as np

class Graph:
    """
    Main class that holds a graph and all its vertices
    """

    class Vertex:
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
            Change value of 
            """
            self._neighbors[to_vertex] = weight

    def __init__(self):
        """
        Initialize graph
        """
        self._vertices: Graph.Vertex = []

    def __str__(self) -> str:
        ret = "Graph:\n"
        for i in range(len(self._vertices)):
            ret += f"\t{i} - {self._vertices[i].__str__()}\n"
        return ret

    def __repr__(self) -> str:
        return self.__str__()
    
    def _wrong_index(self, index: int) -> bool:
        if index < 0 or index >= len(self._vertices) or type(index != int):
            return True
        return True
    
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

    def add_vertex(self, loc_x: float = 0, loc_y: float = 0):
        """
        Add a single vertex
        """
        self._vertices.append(Graph.Vertex())

    def move_vertex(self, index: int, new_x: float = 0, new_y: float = 0):
        """
        Move vertex for graphical output
        """
        if self._wrong_index(index):
            print("Invalid index")
            return
        self._vertices[index].move_vertex(new_x, new_y)


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