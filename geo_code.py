import overpy
import json
from geopy.geocoders import Nominatim

# Khởi tạo Overpass API
api = overpy.Overpass()

# Câu truy vấn Overpass để lấy các địa điểm trong khu vực Giảng Võ
query = """
    area["name"="Giảng Võ, Ba Đình, Hà Nội, Việt Nam"]["boundary"="administrative"];
    (
      node["amenity"](area);
      way["amenity"](area);
      relation["amenity"](area);
    );
    out body;
"""

# Thực hiện truy vấn và lấy dữ liệu
result = api.query(query)

# Lưu các địa điểm và tọa độ vào một danh sách
locations = []

for node in result.nodes:
    locations.append({
        "name": node.tags.get("name", "Unknown"),
        "latitude": node.lat,
        "longitude": node.lon
    })

# In ra các địa điểm
for location in locations:
    print(f"Name: {location['name']}, Latitude: {location['latitude']}, Longitude: {location['longitude']}")

# Lưu vào file JSON
with open("giang_vo_locations.json", "w") as f:
    json.dump(locations, f, indent=4)

# Khởi tạo geolocator từ Geopy
geolocator = Nominatim(user_agent="giang_vo_geocoder")

def geocode_address(address):
    """
    Chuyển địa chỉ thành tọa độ.
    """
    location = geolocator.geocode(address, timeout=10)
    if location:
        return {"address": address, "latitude": location.latitude, "longitude": location.longitude}
    return None

# Geocode các địa điểm lấy từ Overpass API
geocoded_locations = []

for location in locations:
    geocoded = geocode_address(location["name"])
    if geocoded:
        geocoded_locations.append(geocoded)

# Lưu thông tin geocoded vào file JSON
with open("geocoded_giang_vo_locations.json", "w") as f:
    json.dump(geocoded_locations, f, indent=4)

# In thông tin đã geocode
for geocoded_location in geocoded_locations:
    print(f"Address: {geocoded_location['address']}, Latitude: {geocoded_location['latitude']}, Longitude: {geocoded_location['longitude']}")
