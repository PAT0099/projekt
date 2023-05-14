from gm.graphmanager import Graph

def dijkstra(graph: Graph, v_start: int, v_end: int) -> tuple:
    if graph.wrong_index(v_start) or graph.wrong_index(v_end):
        print("Invalid index")
        return
    
    queue = list(range(graph._vertex_count))
    graph.reset_vertex_states([-1, -1])
    graph.at(v_start)._state = [0, -1]

    while len(queue) > 0:
        # find new min
        current_id = -1
        current_dist = -1
        for i in queue:
            dist = graph.at(i)._state[0]
            if dist != -1 and ((dist < current_dist) if current_dist != -1 else True):
                current_id = i
                current_dist = dist

        # check special cases
        if current_id == -1:
            graph.reset_vertex_states()
            return (False, 0, [])
        elif current_id == v_end:
            path_len = graph.at(current_id)._state[0]
            path = [current_id]
            while current_id != v_start:
                prev = graph.at(current_id)._state[1]
                path.append(prev)
                current_id = prev
            return (True, path_len, list(reversed(path)))
        
        # pop min
        queue.pop(queue.index(current_id))
        
        # update neighbors
        for k in graph.at(current_id)._neighbors:
            new_dist = graph.at(current_id)._state[0] + graph.at(current_id)._neighbors[k]
            if (new_dist < graph.at(k)._state[0]) if graph.at(k)._state[0] != -1 else True:
                graph.at(k)._state = [new_dist, current_id]