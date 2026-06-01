# intersections.py
# Finds every point where a major US highway crosses another major highway.
# Uses R-tree spatial indexing to avoid brute-force comparison —
# instead of checking all 583k segments against each other,
# we only check segments whose bounding boxes overlap.
# Output: us_intersections.csv

import os
import warnings
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

warnings.filterwarnings('ignore')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load and filter to just interstates and primary highways
print("Loading highway network...")
gdf = gpd.read_file(os.path.join(BASE_DIR, 'us_highways.geojson'))
print(f"Loaded {len(gdf)} segments")

gdf = gdf[gdf['highway'].isin(['motorway', 'trunk'])].copy()
gdf = gdf.reset_index(drop=True)
print(f"Filtered to {len(gdf)} major highway segments")

# Building spatial index
# Without this, we'd need ~170 billion comparisons for the full dataset
print("Building spatial index...")
sindex = gdf.sindex
print("Done: starting intersection search")

results = []
checked = set()
total = len(gdf)

for i, row in gdf.iterrows():
    if i % 5000 == 0:
        print(f"Progress: {i}/{total} segments — {len(results)} intersections found so far")

    # Only look at segments whose bounding boxes overlap with this one
    candidates = list(sindex.intersection(row.geometry.bounds))

    for j in candidates:
        if i == j:
            continue

        # Skip pairs we've already checked
        pair = tuple(sorted([i, j]))
        if pair in checked:
            continue
        checked.add(pair)

        other = gdf.iloc[j]
        if not row.geometry.intersects(other.geometry):
            continue

        pt = row.geometry.intersection(other.geometry)
        if pt.is_empty:
            continue

        if pt.geom_type == 'Point':
            results.append({
                'lat': pt.y,
                'lon': pt.x,
                'highway_a': row.get('highway', ''),
                'highway_b': other.get('highway', ''),
                'name_a': str(row.get('name', '')),
                'name_b': str(other.get('name', '')),
            })
        elif pt.geom_type == 'MultiPoint':
            for p in pt.geoms:
                results.append({
                    'lat': p.y,
                    'lon': p.x,
                    'highway_a': row.get('highway', ''),
                    'highway_b': other.get('highway', ''),
                    'name_a': str(row.get('name', '')),
                    'name_b': str(other.get('name', '')),
                })

print(f"\nDone! Found {len(results)} intersections")
df = pd.DataFrame(results).drop_duplicates(subset=['lat', 'lon'])
df.to_csv(os.path.join(BASE_DIR, 'us_intersections.csv'), index=False)
print(f"Saved {len(df)} unique intersections")
