# voronoi_clean.py
# Takes raw Voronoi polygons generated in QGIS from the top 5,000 density clusters,
# clips them to the continental US boundary, and calculates area-weighted
# highway intersection density for each polygon.
# A log scale is applied so sparse rural areas still show meaningful color variation.
# Output: voronoi_final.geojson — the final layer used for visualization in QGIS

import os
import numpy as np
import pandas as pd
import geopandas as gpd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

print("Loading files...")
voronoi = gpd.read_file(os.path.join(BASE_DIR, 'voronoi_raw.geojson'))
us = gpd.read_file(os.path.join(BASE_DIR, 'us_boundary.geojson'))
clusters = pd.read_csv(os.path.join(BASE_DIR, 'top5000_clusters.csv'))

# The Voronoi was generated in QGIS so the count field comes through as null
# we re-merge it here from the original clusters file
voronoi['lat'] = voronoi['lat'].astype(float)
voronoi['lon'] = voronoi['lon'].astype(float)
clusters['lat'] = clusters['lat'].astype(float)
clusters['lon'] = clusters['lon'].astype(float)

voronoi = voronoi.merge(clusters[['lat', 'lon', 'count']], on=['lat', 'lon'], how='left', suffixes=('', '_new'))
voronoi['count'] = voronoi['count_new'].fillna(voronoi['count'])
voronoi = voronoi.drop(columns=['count_new'])

# Reproject to Albers Equal Area (EPSG:5070) for accurate area calculation
# Geographic coordinates (degrees) would give distorted areas at US latitudes
voronoi = voronoi.to_crs('EPSG:5070')
us = us.to_crs('EPSG:5070')

# Clip to continental US: removes polygons extending into Canada/Mexico/ocean
print("Clipping to US boundary...")
us_union = us.geometry.union_all()
voronoi['geometry'] = voronoi.geometry.intersection(us_union)
voronoi = voronoi[~voronoi.geometry.is_empty]
voronoi = voronoi[voronoi.geometry.is_valid]

# Calculate polygon area in km2
voronoi['area_km2'] = voronoi.geometry.area / 1_000_000
voronoi['count'] = pd.to_numeric(voronoi['count'], errors='coerce').fillna(1)

# Density = intersections per km2
# Small polygons with high counts = dense urban interchange zones
voronoi['density_score'] = voronoi['count'] / voronoi['area_km2']

# Log scale compresses the extreme outliers (dense urban cores)
# so rural areas still show meaningful variation instead of going flat black
voronoi['density_log'] = np.log1p(voronoi['density_score'])

print(f"Polygons: {len(voronoi)}")
print(f"Area range: {voronoi['area_km2'].min():.1f} to {voronoi['area_km2'].max():.1f} km2")
print(f"Density log range: {voronoi['density_log'].min():.3f} to {voronoi['density_log'].max():.3f}")

# Save back to WGS84 for QGIS compatibility
voronoi = voronoi.to_crs('EPSG:4326')
voronoi.to_file(os.path.join(BASE_DIR, 'voronoi_final.geojson'), driver='GeoJSON')
print("Saved voronoi_final.geojson!")
