import folium
import json

# 서울 중심 좌표
seoul_center = [37.5665, 126.9780]

# 서울 지도 생성
seoul_map = folium.Map(location=seoul_center, zoom_start=10, tiles=None)

# 서울의 각 구에 대한 GeoJSON 파일 경로
geojson_path = "seoul.geojson"

# 서울 구역 정보를 담은 GeoJSON 파일 로드
with open(geojson_path, encoding='utf-8') as f:
    seoul_geojson = json.load(f)

# 서울 구역만 표시하기 위해 지도에 GeoJSON 추가
folium.GeoJson(
    seoul_geojson,
    name="Seoul",
    style_function=lambda x: {'color': 'white', 'fillColor': 'lightgray', 'weight': 2}
).add_to(seoul_map)

# 지도를 HTML 파일로 저장
seoul_map.save("seoul_map.html")
