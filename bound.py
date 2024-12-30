import folium

north = 21.0311603
south = 21.0234381
east = 105.8247374
west = 105.8112969

# Tạo bản đồ ở vị trí trung tâm của khu vực
center_lat = (north + south) / 2
center_lon = (east + west) / 2
mymap = folium.Map(location=[center_lat, center_lon], zoom_start=16)
folium.Rectangle(bounds=[(south, west), (north, east)], color='blue', weight=2.5, opacity=0.5).add_to(mymap)
mymap.save("giang_vo_ba_dinh_map.html")
