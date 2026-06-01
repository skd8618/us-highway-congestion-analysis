import geopandas as gpd
import pandas as pd
import numpy as np

print("Loading files...")
voronoi = gpd.read_file('/Users/snehesh/congestion_env/voronoi_raw.geojson')
us = gpd.read_file('/Users/snehesh/congestion_env/us_boundary.geojson')
clusters = pd.read_csv('/Users/snehesh/congestion_env/top5000_clusters.csv')

# Merge count from clusters
voronoi['lat'] = voronoi['lat'].astype(float)
voronoi['lon'] = voronoi['lon'].astype(float)
clusters['lat'] = clusters['lat'].astype(float)
clusters['lon'] = clusters['lon'].astype(float)

voronoi = voronoi.merge(clusters[['lat','lon','count']], on=['lat','lon'], how='left', suffixes=('','_new'))
voronoi['count'] = voronoi['count_new'].fillna(voronoi['count'])
voronoi = voronoi.drop(columns=['count_new'])

# Reproject to equal area
voronoi = voronoi.to_crs('EPSG:5070')
us = us.to_crs('EPSG:5070')

# Clip to continental US
print("Clipping to US boundary...")
us_union = us.geometry.union_all()
voronoi['geometry'] = voronoi.geometry.intersection(us_union)
voronoi = voronoi[~voronoi.geometry.is_empty]
voronoi = voronoi[voronoi.geometry.is_valid]

# Calculate area in km2
voronoi['area_km2'] = voronoi.geometry.area / 1_000_000
voronoi['count'] = pd.to_numeric(voronoi['count'], errors='coerce').fillna(1)

# Raw density score
voronoi['density_score'] = voronoi['count'] / voronoi['area_km2']

# Log scale so sparse areas still show color variation
voronoi['density_log'] = np.log1p(voronoi['density_score'])

print(f"Polygons: {len(voronoi)}")
print(f"Area range: {voronoi['area_km2'].min():.1f} to {voronoi['area_km2'].max():.1f} km2")
print(f"Density log range: {voronoi['density_log'].min():.3f} to {voronoi['density_log'].max():.3f}")

# Save
voronoi = voronoi.to_crs('EPSG:4326')
voronoi.to_file('/Users/snehesh/congestion_env/voronoi_final.geojson', driver='GeoJSON')
print("\nSaved voronoi_final.geojson!")
