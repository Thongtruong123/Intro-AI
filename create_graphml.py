import osmnx as ox

place_name = "Giảng Võ, Ba Đình, Hà Nội, Vietnam"
G = ox.graph_from_place(place_name, network_type='all')
ox.save_graphml(G, filepath="giang_vo_graph.graphml")

print("File GraphML đã được tạo thành công!")
