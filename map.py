import osmnx as ox
place_name = "Giang Vo, Ba Dinh, Hanoi, Vietnam"
G = ox.graph_from_place(place_name, network_type="all")

ox.save_graphml(G, "giang_vo_graph.graphml")
