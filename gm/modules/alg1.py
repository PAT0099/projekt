from gm.graphmanager import Graph

def bfs(graph: Graph, v_start: int, v_end: int) -> tuple:
    """
    Searches `graph` for a path between vertices given by indices `v_start` and `v_end` using breadth-first search.\n
    Returns a tuple consisting of a bool, float and list.\n
    The bool is `True` if there exists a path between given vertices.
    The float is the length of found path.
    The list shows the order of vertices in found path
    """
    if graph.wrong_index(v_start) or graph.wrong_index(v_end):
        print("Invalid index")
        return
    
    graph.reset_vertex_states(-1)
    queue = [v_start]
    while len(queue) > 0:
        if queue[0] == v_end:
            sum = 0
            return_queue = [queue[0]]
            while return_queue[0] != v_start:
                prev = graph.at(return_queue[0])._state
                sum += graph.at(prev)._neighbors[return_queue[0]]
                return_queue = [prev] + return_queue
            graph.reset_vertex_states()
            return (True, sum, return_queue)

        for i in graph.at(queue[0])._neighbors:
            if graph.at(i)._state == -1:
                queue.append(i)
                graph.at(i)._state = queue[0]
        queue.pop(0)

    graph.reset_vertex_states()
    return (False, 0, [])
    

def dfs(graph: Graph, v_start: int, v_end: int) -> tuple:
    """
    Searches `graph` for a path between vertices given by indices `v_start` and `v_end` using depth-first search.\n
    Returns a tuple consisting of a bool, float and list.\n
    The bool is `True` if there exists a path between given vertices.
    The float is the length of found path.
    The list shows the order of vertices in found path.
    """
    if graph.wrong_index(v_start) or graph.wrong_index(v_end):
        print("Invalid index")
        return
    
    def dfs_vert(current: int):
        graph.at(current)._state = 1
        if current == v_end:
            return (True, 0, [current])
        
        for i in graph.at(current)._neighbors:
            if graph.at(i)._state == 0:
                val = dfs_vert(i)
                if val[0] == True:
                    return (True, graph.at(current)._neighbors[i] + val[1], [current] + val[2])
        return (False, 0, [])
    
    graph.reset_vertex_states()
    ret = dfs_vert(v_start)
    graph.reset_vertex_states()
    return ret
