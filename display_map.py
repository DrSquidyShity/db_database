import folium
import duckdb

DB_DATA_FILE= "db_data.db"

TRAIN_TABLE = "train"
TRAIN_DATA_TABLE = "train_data"

con = duckdb.connect(DB_DATA_FILE)

list = con.sql(f"SELECT latitude, longitude, speed FROM { TRAIN_DATA_TABLE }").fetchall()

if not list:
    print("No data")
    exit()

first_lat, first_lon, _ = list[0]
m = folium.Map(
    location=[first_lat, first_lon],
    zoom_start=12,   # adjust zoom as needed
    tiles='OpenStreetMap'
)

for lat, lon, speed in list:

    if speed >= 200:
        color = 'green'
        opacity = speed / 300
    elif speed >= 100 and speed <200:
        color = 'orange'
        opacity = (speed - 100) / 100
    else:
        color = 'red'
        opacity = speed / 100


    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=opacity,
        stroke=False,
        popup=f"Speed: {speed}"
    ).add_to(m)

m.save('map.html')
