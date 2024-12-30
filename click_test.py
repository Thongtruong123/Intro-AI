import os
import sqlite3
from flask import Flask, render_template_string, request
import folium

# Khởi tạo Flask app
app = Flask(__name__)

# Đường dẫn tới các tile bản đồ offline (bạn cần tải tile từ OSM và lưu vào thư mục 'tiles')
TILE_FOLDER = "tiles"

# Hàm tạo cơ sở dữ liệu geocoding
def create_geocoding_db():
    conn = sqlite3.connect('geocoding.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS addresses (address TEXT, lat REAL, lon REAL)''')
    conn.commit()
    conn.close()

# Hàm thêm địa chỉ và tọa độ vào cơ sở dữ liệu
def insert_address(address, lat, lon):
    conn = sqlite3.connect('geocoding.db')
    c = conn.cursor()
    c.execute("INSERT INTO addresses (address, lat, lon) VALUES (?, ?, ?)", (address, lat, lon))
    conn.commit()
    conn.close()

# Hàm tìm tọa độ từ địa chỉ
def geocode_address(address):
    conn = sqlite3.connect('geocoding.db')
    c = conn.cursor()
    c.execute("SELECT lat, lon FROM addresses WHERE address=?", (address,))
    result = c.fetchone()
    conn.close()
    return result  # Trả về tọa độ (lat, lon) nếu tìm thấy, nếu không trả về None

# Hàm tạo bản đồ với tile từ thư mục offline
def create_map_with_tiles(start_lat, start_lon):
    route_map = folium.Map(location=[start_lat, start_lon], zoom_start=14, tiles=None)
    folium.TileLayer(tiles=f"file:///{os.path.abspath(TILE_FOLDER)}/{{z}}/{{x}}/{{y}}.png", 
                     attr="Map data &copy; OpenStreetMap contributors").add_to(route_map)
    return route_map

# Route chính - Hiển thị bản đồ với tiles offline
@app.route('/')
def index():
    route_map = create_map_with_tiles(21.0278, 105.8367)
    route_map.save("static/route_map.html")
    return render_template_string("""
    <html>
        <head><title>Route Map</title></head>
        <body>
            <iframe src="{{ url_for('static', filename='route_map.html') }}" width="100%" height="600px" style="border:none;"></iframe>
        </body>
    </html>
    """)

# Route tìm đường giữa 2 địa chỉ
@app.route('/find_route', methods=['POST'])
def find_route():
    start_address = request.form.get('start_address')
    end_address = request.form.get('end_address')
    
    # Geocode địa chỉ offline từ cơ sở dữ liệu
    start_point = geocode_address(start_address)
    end_point = geocode_address(end_address)
    
    if not start_point or not end_point:
        return "Không thể tìm thấy địa chỉ trong cơ sở dữ liệu offline."

    # Tạo bản đồ với các điểm bắt đầu và kết thúc
    route_map = create_map_with_tiles(start_point[0], start_point[1])
    
    # Thêm các marker cho các địa chỉ bắt đầu và kết thúc
    folium.Marker([start_point[0], start_point[1]], popup="Start").add_to(route_map)
    folium.Marker([end_point[0], end_point[1]], popup="End").add_to(route_map)

    route_map.save("static/route_map.html")
    return render_template_string("""
    <html>
        <head><title>Route Map</title></head>
        <body>
            <iframe src="{{ url_for('static', filename='route_map.html') }}" width="100%" height="600px" style="border:none;"></iframe>
        </body>
    </html>
    """)

# Chạy ứng dụng Flask
if __name__ == '__main__':
    # Tạo cơ sở dữ liệu geocoding nếu chưa có
    if not os.path.exists('geocoding.db'):
        create_geocoding_db()
        # Thêm một số địa chỉ mẫu vào cơ sở dữ liệu
        insert_address("Giang Vo, Ba Dinh, Hanoi", 21.0278, 105.8367)
        insert_address("Hoan Kiem, Hanoi", 21.0285, 105.8542)
    
    app.run(debug=True)
