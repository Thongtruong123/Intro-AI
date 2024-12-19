import networkx as nx
import heapq
from math import sqrt
# def dijkstra_path(graph, start_node, end_node):
#     """
#     Thuật toán Dijkstra để tìm đường đi ngắn nhất.
#     """
#     try:
#         return nx.shortest_path(graph, source=start_node, target=end_node, weight='length', method='dijkstra')
#     except nx.NetworkXNoPath:
#         raise ValueError("Không tìm được đường đi giữa hai điểm với thuật toán Dijkstra.")

def dijkstra_path(graph, start_node, end_node):
    pq = []  
    heapq.heappush(pq, (0, start_node)) 
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    previous_nodes = {node: None for node in graph.nodes}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end_node:
            break

        for neighbor, data in graph[current_node].items():
            distance = data[0].get('length', 1)  
            new_distance = current_distance + distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    return path[::-1]

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

from collections import deque

def bfs_path(graph, start_node, end_node):
    queue = deque([start_node])
    visited = set()
    previous_nodes = {node: None for node in graph.nodes}

    while queue:
        current_node = queue.popleft()

        if current_node == end_node:
            break

        if current_node not in visited:
            visited.add(current_node)

            for neighbor in graph[current_node]:
                if neighbor not in visited:
                    previous_nodes[neighbor] = current_node
                    queue.append(neighbor)

    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    return path[::-1]

