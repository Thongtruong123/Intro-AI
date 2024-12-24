import osmnx as ox
import folium
place_name = "Giang Vo, Ba Dinh, Hanoi, Vietnam"

G = ox.graph_from_place(place_name, network_type="all")

center = [G.nodes[node]['y'] for node in G.nodes()][0], [G.nodes[node]['x'] for node in G.nodes()][0]
m = folium.Map(location=center, zoom_start=14)

for node in G.nodes:
    lat = G.nodes[node]['y']
    lon = G.nodes[node]['x']
    folium.Marker([lat, lon], popup=f'Node {node}').add_to(m)

m.save("static/giang_vo_map.html")
