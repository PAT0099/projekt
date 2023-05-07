

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
            self.reset_graph()
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

    #spaghetti mess, gets worse the longer you look at it
    def export_svg(self, filename: str, width: int = 500, height: int = 500, vertex_size: float = 25, show_weights: bool = False, show_vertex_ids: bool = False):
        """
        Export graph as svg into a file given by parameter `filename`
        """
        if width <= 0 or height <= 0:
            print("Width and height should be positive values")
            return
        
        try:
            with open(filename, 'w') as f:
                f.write(f'<!-- File generated by GraphManager -->\n<svg width="{width}" height="{height}" stroke-width="{vertex_size/10}" stroke="black" fill="white" version="1.1">')
                # arrow marker, yoinked from https://developer.mozilla.org/en-US/docs/Web/SVG/Element/marker
                f.write(f'\n<defs>\n\t<marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse" fill="black" stroke="none">\n\t\t<path d="M 0 0 L 10 5 L 0 10 z" />\n\t</marker>\n</defs>')
                # text (doesn't align vertically at all times for some reason)
                if show_weights or show_vertex_ids:
                    f.write(f'\n<style>\n\t.num {{\n\t\tfont: {vertex_size}px sans-serif;\n\t\tfill: black;\n\t\tstroke: white;\n\t\tstroke-width: {vertex_size/5};\n\t\tpaint-order: stroke;\n\t\ttext-anchor: middle;\n\t\tdominant-baseline: middle;\n\t}}\n</style>')
                f.write(f'\n<rect width="100%" height="100%" stroke="none" />')

                # draw edges
                weight_data = []
                f.write("\n\n<!-- Edges -->\n<g>\n")
                for v1 in range(self._vertex_count):
                    for v2 in self.at(v1)._neighbors.keys():
                        # get direction, needed for numbers and offset
                        v1x = self.at(v1)._loc_x * width
                        v1y = self.at(v1)._loc_y * height
                        v2x = self.at(v2)._loc_x * width
                        v2y = self.at(v2)._loc_y * height
                        dx = v2x - v1x
                        dy = v2y - v1y
                        l = (dx * dx + dy * dy) ** 0.5
                        # normalize
                        dx = dx / l if l > 0 else 0
                        dy = dy / l if l > 0 else 0
                        
                        if v1 in self.at(v2)._neighbors.keys(): #if there's a connection between v1 and v2 in both ways
                            if v2 < v1: #if connection has been drawn already
                                continue #just move on
                            elif self.at(v1)._neighbors[v2] == self.at(v2)._neighbors[v1]: #if same value
                                # draw double headed arrow
                                x1 = v1x + dx * vertex_size
                                y1 = v1y + dy * vertex_size
                                x2 = v2x - dx * vertex_size
                                y2 = v2y - dy * vertex_size
                                f.write(f'\t<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />\n')
                                if show_weights:
                                    weight_data.append(((x1+x2)/2, (y1+y2)/2, self.at(v1)._neighbors[v2]))

                            else:
                                # draw two arrows
                                sqrt3 = 3**.5
                                half_vs = vertex_size / 2
                                x1 = v1x + sqrt3 * dx * half_vs
                                y1 = v1y + sqrt3 * dy * half_vs
                                x2 = v2x - sqrt3 * dx * half_vs
                                y2 = v2y - sqrt3 * dy * half_vs
                                f.write(f'\t<line x1="{x1 + dy * half_vs}" y1="{y1 - dx * half_vs}" x2="{x2 + dy * half_vs}" y2="{y2 - dx * half_vs}" marker-end="url(#arrow)" />\n')
                                f.write(f'\t<line x1="{x1 - dy * half_vs}" y1="{y1 + dx * half_vs}" x2="{x2 - dy * half_vs}" y2="{y2 + dx * half_vs}" marker-start="url(#arrow)" />\n')
                                if show_weights:
                                    weight_data.append(((x1+x2) / 2 + dy * half_vs, (y1+y2) / 2 - dx * half_vs, self.at(v1)._neighbors[v2]))
                                    weight_data.append(((x1+x2) / 2 - dy * half_vs, (y1+y2) / 2 + dx * half_vs, self.at(v2)._neighbors[v1]))

                        else:
                            # draw single arrow
                            x1 = v1x + dx * vertex_size
                            y1 = v1y + dy * vertex_size
                            x2 = v2x - dx * vertex_size
                            y2 = v2y - dy * vertex_size
                            f.write(f'\t<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" marker-end="url(#arrow)" />\n')
                            if show_weights:
                                weight_data.append(((x1+x2)/2, (y1+y2)/2, self.at(v1)._neighbors[v2]))

                # draw values
                if show_weights:
                    f.write("</g>\n\n<!-- Weights -->\n<g>\n")
                    for w in weight_data:
                        f.write(f'\t<text x="{w[0]}" y="{w[1]}" class="num">{w[2]:g}</text>\n')

                # draw vertices
                f.write("</g>\n\n<!-- Vertices -->\n<g>\n")
                for v in range(self._vertex_count):
                    f.write(f'\t<circle cx="{self.at(v)._loc_x * width}" cy="{self.at(v)._loc_y * height}" r="{vertex_size}" />\n')
                    if show_vertex_ids:
                        f.write(f'\t<text x="{self.at(v)._loc_x * width}" y="{self.at(v)._loc_y * height}" class="num">{v}</text>\n')
                
                f.write("</g>\n</svg>")
        except Exception:
            print("Something went wrong")
