def bellman_ford(graph, start_node, end_node):
    distance = {node: float('inf') for node in graph.nodes}
    distance[start_node] = 0
    previous_nodes = {node: None for node in graph.nodes}

    for _ in range(len(graph.nodes) - 1):
        for node in graph.nodes:
            for neighbor, weight in graph[node]:
                if distance[node] + weight < distance[neighbor]:
                    distance[neighbor] = distance[node] + weight
                    previous_nodes[neighbor] = node


    for node in graph.nodes:
        for neighbor, weight in graph[node]:
            if distance[node] + weight < distance[neighbor]:
                raise ValueError("Graph chứa chu trình âm")

    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    return path[::-1]