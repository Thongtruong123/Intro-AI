# import networkx as nx
# import heapq
# from math import sqrt

# def dijkstra_path(graph, start_node, end_node):
#     pq = []  
#     heapq.heappush(pq, (0, start_node)) 
#     distances = {node: float('inf') for node in graph.nodes}
#     distances[start_node] = 0
#     previous_nodes = {node: None for node in graph.nodes}

#     while pq:
#         current_distance, current_node = heapq.heappop(pq)

#         if current_node == end_node:
#             break

#         for neighbor, data in graph[current_node].items():
#             distance = data[0].get('length', 1)  
#             new_distance = current_distance + distance

#             if new_distance < distances[neighbor]:
#                 distances[neighbor] = new_distance
#                 previous_nodes[neighbor] = current_node
#                 heapq.heappush(pq, (new_distance, neighbor))

#     path = []
#     current = end_node
#     while current is not None:
#         path.append(current)
#         current = previous_nodes[current]
#     return path[::-1]

# def heuristic(node1, node2, graph):
#     x1, y1 = graph.nodes[node1]['x'], graph.nodes[node1]['y']
#     x2, y2 = graph.nodes[node2]['x'], graph.nodes[node2]['y']
#     return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# def nearest_node(G, point, k, heuristic):  
#     nodes = np.array([[G.nodes[n]['x'], G.nodes[n]['y']] for n in G.nodes])
#     distances = np.array([heuristic(G,n, point) for n in G.nodes])
#     nearest_indices = distances.argsort()[:k]
#     nearest_nodes = [list(G.nodes)[i] for i in nearest_indices]
#     nearest_distances = distances[nearest_indices]
#     return nearest_nodes, nearest_distances

# def astar_path(graph, start_node, end_node):
#     pq = []  
#     heapq.heappush(pq, (0, start_node))  
#     distances = {node: float('inf') for node in graph.nodes}
#     distances[start_node] = 0
#     previous_nodes = {node: None for node in graph.nodes}

#     while pq:
#         current_cost, current_node = heapq.heappop(pq)

#         if current_node == end_node:
#             break

#         for neighbor, data in graph[current_node].items():
#             distance = data[0].get('length', 1)
#             tentative_distance = distances[current_node] + distance

#             if tentative_distance < distances[neighbor]:
#                 distances[neighbor] = tentative_distance
#                 priority = tentative_distance + heuristic(neighbor, end_node, graph)
#                 heapq.heappush(pq, (priority, neighbor))
#                 previous_nodes[neighbor] = current_node

#     path = []
#     current = end_node
#     while current is not None:
#         path.append(current)
#         current = previous_nodes[current]
#     return path[::-1]

# from collections import deque

# def bfs_path(graph, start_node, end_node):
#     queue = deque([start_node])
#     visited = set()
#     previous_nodes = {node: None for node in graph.nodes}

#     while queue:
#         current_node = queue.popleft()

#         if current_node == end_node:
#             break

#         if current_node not in visited:
#             visited.add(current_node)

#             for neighbor in graph[current_node]:
#                 if neighbor not in visited:
#                     previous_nodes[neighbor] = current_node
#                     queue.append(neighbor)

#     path = []
#     current = end_node
#     while current is not None:
#         path.append(current)
#         current = previous_nodes[current]
#     return path[::-1]

# def dfs_path(graph, start_node, end_node):
#     stack = [start_node]
#     visited = set()
#     previous_nodes = {node: None for node in graph.nodes}

#     while stack:
#         current_node = stack.pop()

#         if current_node == end_node:
#             break

#         if current_node not in visited:
#             visited.add(current_node)

#             for neighbor in graph[current_node]:
#                 if neighbor not in visited:
#                     previous_nodes[neighbor] = current_node
#                     stack.append(neighbor)

#     path = []
#     current = end_node
#     while current is not None:
#         path.append(current)
#         current = previous_nodes[current]
#     return path[::-1]

# import heapq
# # def bellman_ford_path(graph, start_node, end_node):
# #     path = nx.bellman_ford_path(graph, start_node, end_node, weight='length')
# #     return path

# def bellman_ford(graph, start_node, end_node):
#     distance = {node: float('inf') for node in graph.nodes}
#     distance[start_node] = 0
#     predecessor = {node: None for node in graph.nodes}

#     for _ in range(len(graph.nodes)-1):
#         for u in graph.nodes:
#             for v in graph.neighbors(u):
#                 data = graph[u][v][0]
#                 weight = data.get('length')
#                 if distance[u] != float('inf') and distance[u] + weight < distance[v]:
#                     distance[v] = distance[u] + weight
#                     predecessor[v] = u
#     if distance[end_node] == float('inf'):
#         return None, None
#     path = []
#     current_node = end_node
#     while current_node is not None:
#         path.append(current_node)
#         current_node = predecessor[current_node]
#     path.reverse()

#     return path, distance[end_node]
# import numpy as np

import osmnx as ox 
import networkx as nx
import heapq
import numpy as np
from math import sqrt


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

import osmnx as ox 
import networkx as nx
import json

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


# A* Algorithm
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
            distance = data.get('length', 1)
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




# DFS Algorithm


# Bellman-Ford Algorithm
def bellman_ford(graph, start_node, end_node):
    distance = {node: float('inf') for node in graph.nodes}
    distance[start_node] = 0
    predecessor = {node: None for node in graph.nodes}

    for _ in range(len(graph.nodes)-1):
        for u in graph.nodes:
            for v in graph.neighbors(u):
                weight = graph[u][v].get('length', 1)
                if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                    distance[v] = distance[u] + weight
                    predecessor[v] = u

    for u in graph.nodes:
        for v in graph.neighbors(u):
            weight = graph[u][v].get('length', 1)
            if distance[u] != float('inf') and distance[u] + weight < distance[v]:
                raise ValueError("Graph contains a negative-weight cycle")

    if distance[end_node] == float('inf'):
        return None, None

    path = []
    current_node = end_node
    while current_node is not None:
        path.append(current_node)
        current_node = predecessor[current_node]
    path.reverse()

    return path, distance[end_node]

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
def heuristic(node1, node2, graph):
    """Calculate Euclidean distance heuristic between two nodes"""
    x1, y1 = graph.nodes[node1]['x'], graph.nodes[node1]['y']
    x2, y2 = graph.nodes[node2]['x'], graph.nodes[node2]['y']
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def a_star(graph, start_node, end_node, heuristic=heuristic):
    """A* pathfinding algorithm implementation"""
    # Priority queue of nodes to visit, with f-score as priority
    open_set = {start_node}
    closed_set = set()
    
    # Dictionary to store g-scores (cost from start to node)
    g_score = {node: float('inf') for node in graph.nodes}
    g_score[start_node] = 0
    
    # Dictionary to store f-scores (g_score + heuristic)
    f_score = {node: float('inf') for node in graph.nodes}
    f_score[start_node] = heuristic(start_node, end_node, graph)
    
    # Dictionary to store path
    came_from = {node: None for node in graph.nodes}
    
    while open_set:
        # Get node with minimum f_score
        current = min(open_set, key=lambda x: f_score[x])
        
        if current == end_node:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1], g_score[end_node]
            
        open_set.remove(current)
        closed_set.add(current)
        
        for neighbor in graph[current]:
            if neighbor in closed_set:
                continue
                
            # Calculate tentative g_score
            tentative_g_score = g_score[current] + graph[current][neighbor][0].get('length', 1)
            
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue
                
            # This path is the best until now
            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_node, graph)
    
    return None, None 
def bfs(graph, start_node, end_node):
    """Breadth-first search algorithm implementation"""
    # Queue for BFS traversal
    queue = [start_node]
    
    # Set to track visited nodes
    visited = {start_node}
    
    # Dictionary to store path
    came_from = {node: None for node in graph.nodes}
    
    # Dictionary to store distances
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    
    while queue:
        current = queue.pop(0)
        
        if current == end_node:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1], distances[end_node]
            
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                came_from[neighbor] = current
                distances[neighbor] = distances[current] + graph[current][neighbor][0].get('length', 1)
                
    return None, None

from math import radians, cos, sin, asin, sqrt

def heuristic(graph, node, goal):
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
    # for i in range(k):
    #     print(f"Node: {nearest_nodes[i]}, Distance: {nearest_distances[i]}")
    return nearest_nodes, nearest_distances