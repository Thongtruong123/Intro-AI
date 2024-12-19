from math import sqrt
import heapq

def heuristic(node1, node2, graph):
    x1, y1 = graph.nodes[node1]['x'], graph.nodes[node1]['y']
    x2, y2 = graph.nodes[node2]['x'], graph.nodes[node2]['y']
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def astar_path(graph, start_node, end_node):
    pq = []  
    heapq.heappush(pq, (0, start_node))  
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph.nodes}

    while pq:
        current_cost, current_node = heapq.heappop(pq)

        if current_node == end_node:
            break

        for neighbor, data in graph[current_node].items():
            distance = data[0].get('length', 1)
            tentative_distance = distances[current_node] + distance

            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
                priority = tentative_distance + heuristic(neighbor, end_node, graph)
                heapq.heappush(pq, (priority, neighbor))
                previous_nodes[neighbor] = current_node

    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    return path[::-1]
