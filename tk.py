from flask import Flask, request, jsonify, render_template_string
import osmnx as ox
import folium
from algorithm import dijkstra_path, astar_path, bfs_path, bellman_ford_path, dfs_path

app = Flask(__name__)

# Tải dữ liệu đồ thị và lưu vào file graphml để sử dụng offline
try:
    G = ox.load_graphml("giang_vo_graph.graphml")
except FileNotFoundError:
    place_name = "Giang Vo, Ba Dinh, Hanoi, Vietnam"
    G = ox.graph_from_place(place_name, network_type="drive")
    ox.save_graphml(G, "giang_vo_graph.graphml")

# Tạo bản đồ Folium với đường bao đồ thị G
def create_map_with_boundary(G):
    # Tạo bản đồ Folium, lấy trung tâm từ một node ngẫu nhiên
    node = list(G.nodes())[0]
    m = folium.Map(location=[G.nodes[node]['y'], G.nodes[node]['x']], zoom_start=14)

    # Vẽ các cạnh của đồ thị lên bản đồ
    for u, v, data in G.edges(data=True):
        lat_u, lon_u = G.nodes[u]['y'], G.nodes[u]['x']
        lat_v, lon_v = G.nodes[v]['y'], G.nodes[v]['x']
        
        # Vẽ đường nối giữa hai điểm
        folium.PolyLine(
            locations=[(lat_u, lon_u), (lat_v, lon_v)],
            color='blue',
            weight=1.5
        ).add_to(m)

    return m


@app.route('/')
def index():
    # Tạo bản đồ với đường bao của đồ thị
    map_with_boundary = create_map_with_boundary(G)
    
    map_html = map_with_boundary._repr_html_()
    
    return render_template_string("""
        <html>
            <head><title>Map of Giang Vo</title></head>
            <body>
                <h1>Map of Giang Vo, Hanoi</h1>
                {{ map_html|safe }}
            </body>
        </html>
    """, map_html=map_html)

# Các route khác như dijkstra, astar sẽ không thay đổi

if __name__ == '__main__':
    app.run(debug=True)
