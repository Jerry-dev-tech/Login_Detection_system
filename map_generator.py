import pandas as pd
import folium

# Read dataset
df = pd.read_csv("Dataset/login_data.csv")

# Create world map
m = folium.Map(
    location=[20, 0],
    zoom_start=2
)

# Add markers
for _, row in df.iterrows():

    folium.Marker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        popup=f"""
        User: {row['Username']}
        <br>
        Country: {row['Country']}
        <br>
        City: {row['City']}
        """
    ).add_to(m)

# Save map
m.save("static/login_map.html")

print("Map Created Successfully")
