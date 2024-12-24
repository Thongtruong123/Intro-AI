from flask import Flask, request, jsonify, render_template_string
import osmnx as ox
import folium
from algorithm import dijkstra_path, astar_path, bfs_path, bellman_ford_path, dfs_path

app = Flask(__name__)

try:
    G = ox.load_graphml("giang_vo_graph.graphml")
except FileNotFoundError:
    place_name = "Giang Vo, Ba Dinh, Hanoi, Vietnam"
    G = ox.graph_from_place(place_name, network_type="drive")
    ox.save_graphml(G, "giang_vo_graph.graphml")

def geocode_address(address):
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
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Route Finder</title>
        <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
        <style>
            body {
                font-family: 'Roboto', Arial, sans-serif;
                background-color: #f1f3f4;
                margin: 0;
                padding: 0;
                color: #202124;
            }
            .container {
                display: flex;
                height: 100vh;
            }
            .sidebar {
                width: 400px;
                background-color: white;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                padding: 20px;
                overflow-y: auto;
            }
            .map-container {
                flex-grow: 1;
                background-color: #e0e0e0;
            }
            h1 {
                color: #1a73e8;
                font-size: 24px;
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }
            label {
                font-weight: 500;
                color: #5f6368;
            }
            input[type="text"] {
                padding: 10px;
                font-size: 16px;
                border: 1px solid #dadce0;
                border-radius: 4px;
                outline: none;
                transition: border-color 0.3s;
            }
            input[type="text"]:focus {
                border-color: #1a73e8;
            }
            .radio-group {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            .radio-button {
                display: flex;
                align-items: center;
                cursor: pointer;
            }
            .radio-button input {
                display: none;
            }
            .radio-button span {
                padding: 8px 16px;
                background-color: #f1f3f4;
                border-radius: 16px;
                transition: background-color 0.3s, color 0.3s;
            }
            .radio-button input:checked + span {
                background-color: #1a73e8;
                color: white;
            }
            button {
                background-color: #1a73e8;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 4px;
                cursor: pointer;
                transition: background-color 0.3s;
            }
            button:hover {
                background-color: #1765cc;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="sidebar">
                <h1>Route Finder</h1>
                <form action="/find_route" method="post">
                    <label for="start_address">Địa chỉ bắt đầu:</label>
                    <input type="text" name="start_address" id="start_address" required placeholder="Nhập địa chỉ bắt đầu">

                    <label for="end_address">Địa chỉ kết thúc:</label>
                    <input type="text" name="end_address" id="end_address" required placeholder="Nhập địa chỉ kết thúc">

                    <label>Chọn thuật toán:</label>
                    <div class="radio-group">
                        <label class="radio-button">
                            <input type="radio" name="algorithm" value="dijkstra" checked>
                            <span>Dijkstra</span>
                        </label>
                        <label class="radio-button">
                            <input type="radio" name="algorithm" value="astar">
                            <span>A*</span>
                        </label>
                        <label class="radio-button">
                            <input type="radio" name="algorithm" value="bfs">
                            <span>BFS</span>
                        </label>
                        <label class="radio-button">
                            <input type="radio" name="algorithm" value="dfs">
                            <span>DFS</span>
                        </label>
                        <label class="radio-button">
                            <input type="radio" name="algorithm" value="bellman_ford">
                            <span>Bellman-Ford</span>
                        </label>
                    </div>

                    <button type="submit">Tìm đường</button>
                </form>
            </div>
            <div class="map-container" id="map">
                
            </div>
        </div>
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

    if not start_point :
        return "Không thể tìm tọa độ cho  địa chỉ {start_point}. Vui lòng thử lại."
    if not end_point :
        return "Không thể tìm tọa độ cho  địa chỉ {end_point}. Vui lòng thử lại."

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
            route = bellman_ford_path(G, start_node, end_node)
        else:
            return "Thuật toán không hợp lệ."

        route_length = sum(G[u][v][0]['length'] for u, v in zip(route[:-1], route[1:]))

        route_map = folium.Map(location=start_point, zoom_start=14)

        # Thêm các điểm bắt đầu và kết thúc vào bản đồ
        folium.Marker(start_point, popup="Start: {}".format(start_address), icon=folium.Icon(color='green')).add_to(route_map)
        folium.Marker(end_point, popup="End: {}".format(end_address), icon=folium.Icon(color='red')).add_to(route_map)

        # Thêm tuyến đường vào bản đồ
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(route_coords, color="#1a73e8", weight=5, opacity=0.7).add_to(route_map)

        # Lưu bản đồ vào file HTML
        route_map.save("route_map.html")

        # Trả về kết quả với độ dài đường đi và hiển thị trực tiếp bản đồ
        return render_template_string("""
        <!DOCTYPE html>
        <html lang="vi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Route Result</title>
            <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
            <style>
                body {
                    font-family: 'Roboto', Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    color: #202124;
                    display: flex;
                    height: 100vh;
                }
                .sidebar {
                    width: 300px;
                    background-color: white;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    padding: 20px;
                    overflow-y: auto;
                }
                .map-container {
                    flex-grow: 1;
                }
                h1 {
                    color: #1a73e8;
                    font-size: 24px;
                    margin-bottom: 20px;
                }
                p {
                    margin-bottom: 10px;
                }
                .result-item {
                    background-color: #f1f3f4;
                    border-radius: 4px;
                    padding: 10px;
                    margin-bottom: 10px;
                }
                iframe {
                    border: none;
                    width: 100%;
                    height: 100%;
                }
            </style>
        </head>
        <body>
            <div class="sidebar">
                <h1>Kết quả tìm đường</h1>
                <div class="result-item">
                    <p><strong>Từ:</strong> {{ start_address }}</p>
                    <p><strong>Đến:</strong> {{ end_address }}</p>
                </div>
                <div class="result-item">
                    <p><strong>Thuật toán:</strong> {{ algorithm.upper() }}</p>
                    <p><strong>Độ dài tuyến đường:</strong> {{ "%.2f"|format(route_length / 1000) }} km</p>
                </div>
            </div>
            <div class="map-container">
                <iframe src="/view_map"></iframe>
            </div>
        </body>
        </html>
        """, start_address=start_address, end_address=end_address, algorithm=algorithm, route_length=route_length)

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