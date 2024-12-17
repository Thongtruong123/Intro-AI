from flask import Flask, request, jsonify, render_template_string
import osmnx as ox
import networkx as nx
import folium

app = Flask(__name__)

# Lấy đồ thị giao thông cho khu vực Giảng Võ
place_name = "Giang Vo, Ba Dinh, Hanoi, Vietnam"
G = ox.graph_from_place(place_name, network_type= "all")

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
    Giao diện người dùng với form nhập 2 địa chỉ.
    """
    html = """
    <!doctype html>
    <title>Route Finder</title>
    <h1>Nhập địa chỉ để tìm đường đi</h1>
    <form action="/find_route" method="post">
        Địa chỉ bắt đầu: <input type="text" name="start_address"><br>
        Địa chỉ kết thúc: <input type="text" name="end_address"><br>
        <input type="submit" value="Tìm đường">
    </form>
    """
    return render_template_string(html)

@app.route('/find_route', methods=['POST'])
def find_route():
    """
    Xử lý tìm đường giữa hai địa chỉ.
    """
    start_address = request.form.get('start_address')
    end_address = request.form.get('end_address')

    # Geocode các địa chỉ
    start_point = geocode_address(start_address)
    end_point = geocode_address(end_address)

    if not start_point or not end_point:
        return "Không thể tìm tọa độ cho một trong hai địa chỉ. Vui lòng thử lại."

    # Tìm nút gần nhất trong đồ thị
    try:
        start_node = ox.distance.nearest_nodes(G, start_point[1], start_point[0])
        end_node = ox.distance.nearest_nodes(G, end_point[1], end_point[0])

        # Kiểm tra kết nối của đồ thị
        print(f"Start node: {start_node}, End node: {end_node}")

        # Tìm đường đi ngắn nhất với Dijkstra's algorithm
        route = nx.shortest_path(G, start_node, end_node, weight="length", method='dijkstra')

        # Tính độ dài của tuyến đường bằng cách cộng chiều dài các cạnh trong lộ trình
        route_length = 0
        for i in range(len(route) - 1):
            u, v = route[i], route[i+1]
            route_length += G[u][v][0]['length']  # Lấy độ dài từ đồ thị G

        # Tạo bản đồ Folium
        route_map = folium.Map(location=start_point, zoom_start=14)

        # Thêm các điểm bắt đầu và kết thúc vào bản đồ
        folium.Marker(start_point, popup="Start: {}".format(start_address)).add_to(route_map)
        folium.Marker(end_point, popup="End: {}".format(end_address)).add_to(route_map)

        # Thêm tuyến đường vào bản đồ
        route_coords = [(G.nodes[node]['y'], G.nodes[node]['x']) for node in route]
        folium.PolyLine(route_coords, color="blue", weight=2.5, opacity=1).add_to(route_map)

        # Lưu bản đồ vào file HTML
        route_map.save("route_map.html")

        # Trả về kết quả với độ dài đường đi
        return """
        <h1>Kết quả:</h1>
        <p>Đường đi từ: {} đến {}</p>
        <p>Độ dài tuyến đường: {:.2f} km</p>
        <a href="/view_map" target="_blank">Xem bản đồ</a>
        """.format(start_address, end_address, route_length / 1000)  # Đổi từ mét sang km

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
        return f"Lỗi khi tải bản đồ: {e}"

if __name__ == '__main__':
    app.run(debug=True)
