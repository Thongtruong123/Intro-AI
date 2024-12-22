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
    G = ox.graph_from_place(place_name, network_type="all")
    ox.save_graphml(G, "giang_vo_graph.graphml")

def geocode_address(address):
    """
    Hàm chuyển địa chỉ thành tọa độ.
    """
    try:
        point = ox.geocode(address)
        return point
    except Exception as e:
        return None

@app.route('/')
def index():
    """
    Giao diện người dùng với form nhập 2 địa chỉ và chọn thuật toán.
    """
    html = """
    <!doctype html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Route Finder</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 0;
                color: #333;
            }
            .container {
                width: 100%;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #4CAF50;
                text-align: center;
                font-size: 2rem;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            label {
                font-weight: bold;
                font-size: 1.1rem;
            }
            input[type="text"] {
                padding: 10px;
                font-size: 1rem;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            input[type="radio"] {
                margin-right: 5px;
            }
            .form-actions {
                display: flex;
                justify-content: center;
            }
            input[type="submit"] {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 1rem;
            }
            input[type="submit"]:hover {
                background-color: #45a049;
            }
            footer {
                text-align: center;
                font-size: 0.9rem;
                color: #777;
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Nhập địa chỉ để tìm đường đi</h1>
            <form action="/find_route" method="post">
                <label for="start_address">Địa chỉ bắt đầu:</label>
                <input type="text" name="start_address" id="start_address" required><br>

                <label for="end_address">Địa chỉ kết thúc:</label>
                <input type="text" name="end_address" id="end_address" required><br>

                <label>Chọn thuật toán:</label>
                <input type="radio" name="algorithm" value="dijkstra" checked> Dijkstra<br>
                <input type="radio" name="algorithm" value="astar"> A*<br>
                <input type="radio" name="algorithm" value="bfs"> BFS<br>
                <input type="radio" name="algorithm" value="dfs"> DFS<br>
                <input type="radio" name="algorithm" value="bellman_ford"> Bellman_ford<br>

                <div class="form-actions">
                    <input type="submit" value="Tìm đường">
                </div>
            </form>
        </div>
        <footer>
            <p>© 2024 Route Finder. All rights reserved.</p>
        </footer>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/find_route', methods=['POST'])
def find_route():
    """
    Xử lý tìm đường giữa hai địa chỉ.
    """
    start_address = request.form.get('start_address')
    end_address = request.form.get('end_address')
    algorithm = request.form.get('algorithm')

    # Geocode các địa chỉ
    start_point = geocode_address(start_address)
    end_point = geocode_address(end_address)

    if not start_point or not end_point:
        return "Không thể tìm tọa độ cho một trong hai địa chỉ. Vui lòng thử lại."

    try:
        start_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])
        end_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])

        if algorithm == "dijkstra":
            route = dijkstra_path(G, start_node, end_node)
        elif algorithm == "astar":
            route = astar_path(G, start_node, end_node)
        elif algorithm == "bfs":
            route = bfs_path(G, start_node, end_node)
        elif algorithm == "dfs":
            route = dfs_path(G, start_node, end_node)
        elif algorithm == "bellman_ford":
            route = dijkstra_path(G, start_node, end_node)
        else:
            return "Thuật toán không hợp lệ."

        route_length = sum(G[u][v][0]['length'] for u, v in zip(route[:-1], route[1:]))

        route_map = folium.Map(location=start_point, zoom_start=14)

        # Thêm các điểm bắt đầu và kết thúc vào bản đồ
        folium.Marker(start_point, popup="Start: {}".format(start_address), icon=folium.Icon(color='green')).add_to(route_map)
        folium.Marker(end_point, popup="End: {}".format(end_address), icon=folium.Icon(color='green')).add_to(route_map)

        # Thêm tuyến đường vào bản đồ
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(route_map)

        # Đánh dấu tất cả các điểm trên tuyến đường
        for coord in route_coords:
            folium.CircleMarker(location=coord, radius=3, color='red', fill=True).add_to(route_map)

        # Lưu bản đồ vào file HTML
        route_map.save("route_map.html")

        # Trả về kết quả với độ dài đường đi và hiển thị trực tiếp bản đồ
        return render_template_string("""
        <h1>Kết quả:</h1>
        <p>Đường đi từ: {} đến {}</p>
        <p>Thuật toán: {}</p>
        <p>Độ dài tuyến đường: {:.2f} km</p>
        <h3>Đây là bản đồ tuyến đường:</h3>
        <iframe src="/view_map" width="100%" height="600px"></iframe>
        """.format(start_address, end_address, algorithm.upper(), route_length / 1000))

    except Exception as e:
        return f"Lỗi khi tìm đường: {e}"

@app.route('/view_map')
def view_map():
    """
    Hiển thị bản đồ đã lưu.
    """
    try:
        with open("route_map.html", "r", encoding="utf-8") as file:
            content = file.read()
        return content
    except Exception as e:
        return f"Lỗi khi load bản đồ: {e}"

if __name__ == '__main__':
    app.run(debug=True)
