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
