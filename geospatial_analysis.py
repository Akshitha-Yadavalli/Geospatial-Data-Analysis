import pandas as pd
import matplotlib.pyplot as plt
import folium
import os

output_folder = "output"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

df = pd.read_csv("sales_locations.csv")

# Remove duplicates
df.drop_duplicates(inplace=True)

# Save cleaned data
df.to_csv(f"{output_folder}/cleaned_sales_data.csv", index=False)

# Sales by City
plt.figure(figsize=(10,5))
plt.bar(df["City"], df["Sales"])
plt.xticks(rotation=45)
plt.title("Sales by City")
plt.tight_layout()
plt.savefig(f"{output_folder}/sales_by_city.png")
plt.close()

# Demand Analysis
plt.figure(figsize=(10,5))
plt.bar(df["City"], df["DemandScore"])
plt.xticks(rotation=45)
plt.title("Demand Score by City")
plt.tight_layout()
plt.savefig(f"{output_folder}/demand_analysis.png")
plt.close()

# Create Interactive Map
india_map = folium.Map(location=[20.5937,78.9629], zoom_start=5)

for _, row in df.iterrows():
    folium.Marker(
        [row["Latitude"], row["Longitude"]],
        popup=f"{row['City']} | Sales: {row['Sales']} | Demand: {row['DemandScore']}",
        tooltip=row["City"]
    ).add_to(india_map)

india_map.save(f"{output_folder}/business_expansion_map.html")

# Expansion Opportunities
expansion = df[
    (df["DemandScore"] > 90) &
    (df["ExistingStores"] <= 1)
]

with open(f"{output_folder}/geospatial_report.txt", "w") as report:
    report.write("GEOSPATIAL DATA ANALYSIS REPORT\n")
    report.write("===============================\n\n")

    report.write("Recommended Expansion Locations:\n\n")

    for city in expansion["City"]:
        report.write(f"- {city}\n")

print("Geospatial Analysis Completed Successfully!")