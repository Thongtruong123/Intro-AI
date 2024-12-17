import networkx as nx

def dijkstra_path(graph, start_node, end_node):
    """
    Thuật toán Dijkstra để tìm đường đi ngắn nhất.
    """
    try:
        return nx.shortest_path(graph, source=start_node, target=end_node, weight='length', method='dijkstra')
    except nx.NetworkXNoPath:
        raise ValueError("Không tìm được đường đi giữa hai điểm với thuật toán Dijkstra.")

def astar_path(graph, start_node, end_node):
    """
    Thuật toán A* để tìm đường đi ngắn nhất.
    """
    try:
        return nx.astar_path(graph, source=start_node, target=end_node, heuristic=lambda u, v: 0, weight='length')
    except nx.NetworkXNoPath:
        raise ValueError("Không tìm được đường đi giữa hai điểm với thuật toán A*.")

def bfs_path(graph, start_node, end_node):
    """
    Thuật toán BFS để tìm đường đi ngắn nhất (không có trọng số).
    """
    try:
        return nx.shortest_path(graph, source=start_node, target=end_node, method='unweighted')
    except nx.NetworkXNoPath:
        raise ValueError("Không tìm được đường đi giữa hai điểm với thuật toán BFS.")
