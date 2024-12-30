import osmnx as ox

north = 21.0311603
south = 21.0234381
east = 105.8247374
west = 105.8112969

bbox = (north, south, east, west)

G = ox.graph_from_bbox(bbox, network_type='all')
ox.save_graphml(G, filepath='giang_vo_ba_dinh_graph.graphml')

print("Tệp GraphML đã được lưu thành công.")
