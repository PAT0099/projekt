from graphmanager import Graph
from math import sin, pi

def add_complete(g: Graph, n: int, weight: float, x: float = 0.5, y: float = 0.5, radius: float = 0.4, angle: float = 0):
    m = g._vertex_count
    for i in range(n):
        g.add_vertex(x + radius * sin(2*pi * (i/n) + angle), y - radius * sin(2*pi * (.25 + i/n) + angle))
        for v in range(m, m+i):
            g.set_connection(m+i, v, weight, True)

def add_cycle(g: Graph, n: int, weight: float, x: float = 0.5, y: float = 0.5, radius: float = 0.4, angle: float = 0):
    m = g._vertex_count
    for i in range(n):
        g.add_vertex(x + radius * sin(2*pi * (i/n) + angle), y - radius * sin(2*pi * (.25 + i/n) + angle))
        if i > 0:
            g.set_connection(m+i, m+i-1, weight, True)
    g.set_connection(m, m+n-1, weight, True)

def add_path(g: Graph, n: int, weight: float, x: float = 0.5, y: float = 0.5, length: float = 0.4, angle: float = 0):
    m = g._vertex_count
    for i in range(n):
        g.add_vertex(x + length * i/(n-1) * sin(pi/2 - angle), y + length * i/(n-1) * sin(-angle))
        if i > 0:
            g.set_connection(m+i, m+i-1, weight, True)
