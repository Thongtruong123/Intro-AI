import osmnx as ox 
import numpy as np 
import networkx as nx
import heapq
import itertools

import json
import numpy as np 
def bellman_ford(graph, start_node, end_node):
    distance = {node: float('inf') for node in graph.nodes}
    distance[start_node] = 0
    predecessor = {node: None for node in graph.nodes}

    for _ in range(len(graph.nodes)-1):
        for u in graph.nodes:
            for v in graph.neighbors(u):
                data = graph[u][v][0]
                weight = data.get('length')
                if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    predecessor[v] = u
    if distance[end_node] == float('inf'):
        return None, None
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = predecessor[current_node]
    path.reverse()

    return path, distance[end_node]


from math import radians, cos, sin, asin, sqrt
def heuristic(graph, node, goal):
    node_x, node_y = graph.nodes[node]['x'], graph.nodes[node]['y']
    goal_x, goal_y = graph.nodes[goal]['x'], graph.nodes[goal]['y']
    lon1, lat1, lon2, lat2 = map(radians, [node_x, node_y, goal_x, goal_y])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000
    return c * r

def heuristic_node(graph, node, goal):
    # Calculate the great-circle distance between two points on the Earth, haversine formula
    node_x, node_y = graph.nodes[node]['x'], graph.nodes[node]['y']
    goal_x, goal_y = goal[0], goal[1]
    lon1, lat1, lon2, lat2 = map(radians, [node_x, node_y, goal_x, goal_y])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371000
    return c * r
def nearest_node(G, point, k, heuristic):
    
    nodes = np.array([[G.nodes[n]['x'], G.nodes[n]['y']] for n in G.nodes])
    distances = np.array([heuristic(G,n, point) for n in G.nodes])
    nearest_indices = distances.argsort()[:k]
    nearest_nodes = [list(G.nodes)[i] for i in nearest_indices]
    nearest_distances = distances[nearest_indices]
    return nearest_nodes, nearest_distances




def dijkstra(graph, start_node, end_node):
    distances = {node: float('infinity') for node in graph.nodes()}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]
    previous_nodes = {node: None for node in graph.nodes()}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, attributes in graph[current_node].items():
            distance = current_distance + attributes[0].get('length')
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    if distances[end_node] == float('infinity'):
        return None, None
    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = previous_nodes[current_node]
    path.reverse()
    return path, distances[end_node]

def dfs(graph, start_node, goal, path=None, visited=None):
    # path is the path from the start node to the current node 
    if path is None:
        path = []
    if visited is None:
        visited = set()
    
    path.append(start_node)
    visited.add(start_node)
    if start_node == goal:
        return path
    
    for neighbor in graph.neighbors(start_node):
        if neighbor not in visited:
            result = dfs(graph, neighbor, goal, path, visited)
            if result is not None:
                return result
    path.pop() # backtrack
    return None

    


def bfs(graph, start_node, end_node):
    queue = [(start_node, [start_node])]
    visited = set()

    while queue:
        current_node, path = queue.pop(0)
        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node == end_node:
            path_length = sum(graph[path[i]][path[i + 1]][0].get('length') for i in range(len(path) - 1))
            return path, path_length

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))

    return None, None


def a_star(graph, start_node, end_node, heuristic):
    open_set = []
    c = itertools.count()
    heapq.heappush(open_set, (0, next(c), start_node)) 

    came_from = {}  # To reconstruct the path
    g_score = {node: float('inf') for node in graph.nodes} 
    g_score[start_node] = 0
    f_score = {node: float('inf') for node in graph.nodes}  
    f_score[start_node] = heuristic(graph, start_node, end_node)

    enqueued = {}

    while open_set:
        _, _, current = heapq.heappop(open_set) 

        if current == end_node:
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.append(current)
            return path[::-1], g_score[end_node]

        for neighbor in graph.neighbors(current):
            weight = graph[current][neighbor][0].get('length', 1)
            tentative_g_score = g_score[current] + weight
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(graph, neighbor, end_node)

                if neighbor not in enqueued or tentative_g_score < enqueued[neighbor]:
                    enqueued[neighbor] = tentative_g_score
                    heapq.heappush(open_set, (f_score[neighbor], next(c), neighbor))

    return None, None