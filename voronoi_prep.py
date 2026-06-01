import pandas as pd

df = pd.read_csv('/Users/snehesh/congestion_env/us_intersections.csv')

# Remove Alaska and Hawaii — keep continental US only
df = df[(df['lat'] >= 24) & (df['lat'] <= 50)]
df = df[(df['lon'] >= -125) & (df['lon'] <= -65)]

print(f"Continental US intersections: {len(df)}")

# Round coordinates to cluster nearby intersections
df['lat_r'] = df['lat'].round(2)
df['lon_r'] = df['lon'].round(2)

# Count intersections per cluster cell
density = df.groupby(['lat_r','lon_r']).size().reset_index(name='count')
density = density.rename(columns={'lat_r':'lat','lon_r':'lon'})

# Keep top 5000 densest clusters
top5000 = density.nlargest(5000, 'count')

print(f"Top 5000 density clusters ready")
print(f"Max density: {top5000['count'].max()} intersections per cell")
print(f"Min density: {top5000['count'].min()} intersections per cell")

top5000.to_csv('/Users/snehesh/congestion_env/top5000_clusters.csv', index=False)
print("Saved!")
