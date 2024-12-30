import osmnx as ox
from geopy.geocoders import Nominatim
import json
import time

# Tải đồ thị từ file graphml
G = ox.load_graphml("giang_vo_graph.graphml")

# Trích xuất tất cả các tọa độ từ đồ thị
nodes = list(G.nodes(data=True))
coordinates = [(data['y'], data['x']) for _, data in nodes]

# Khởi tạo geolocator
geolocator = Nominatim(user_agent="geo_converter")

# Lưu địa chỉ
address_lookup = {}

# Geocode cho từng tọa độ
for lat, lon in coordinates:
    try:
        location = geolocator.reverse((lat, lon))
        address = location.address if location else "Không tìm thấy địa chỉ"
        address_lookup[f"{lat},{lon}"] = address
        time.sleep(1)  # Tránh bị chặn do gọi API quá nhiều
    except Exception as e:
        address_lookup[f"{lat},{lon}"] = "Không tìm thấy địa chỉ"

# Lưu kết quả vào file JSON
with open('address_lookup.json', 'w', encoding='utf-8') as file:
    json.dump(address_lookup, file, ensure_ascii=False, indent=4)

# Tải dữ liệu từ file JSON
with open('address_lookup.json', 'r', encoding='utf-8') as file:
    address_lookup = json.load(file)

# Hàm tìm địa chỉ từ tọa độ
def geocode_offline(lat, lon):
    key = f"{lat},{lon}"
    return address_lookup.get(key, "Không tìm thấy địa chỉ")

# Cập nhật địa chỉ vào dữ liệu node trong đồ thị
for node_id, data in G.nodes(data=True):
    lat, lon = data['y'], data['x']
    data['address'] = geocode_offline(lat, lon)

# In thử một số node để xác minh dữ liệu
for node_id, data in G.nodes(data=True):
    print(f"Node {node_id}: {data['address']}")
    break
