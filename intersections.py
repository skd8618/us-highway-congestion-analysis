import geopandas as gpd
import pandas as pd
from shapely.ops import unary_union
import warnings
warnings.filterwarnings('ignore')

print("Loading highway network...")
gdf = gpd.read_file('/Users/snehesh/congestion_env/us_highways.geojson')
print(f"Loaded {len(gdf)} segments")
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, box
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print("Loading highway network...")
gdf = gpd.read_file('/Users/snehesh/congestion_env/us_highways.geojson')
print(f"Loaded {len(gdf)} segments")

gdf = gdf[gdf['highway'].isin(['motorway', 'trunk'])].copy()
gdf = gdf.reset_index(drop=True)
print(f"Filtered to {len(gdf)} major highway segments")

# Build spatial index once for entire dataset
print("Building spatial index...")
sindex = gdf.sindex
print("Spatial index built!")

results = []
checked = set()

print("Finding intersections...")
total = len(gdf)

for i, row in gdf.iterrows():
    if i % 5000 == 0:
        print(f"Progress: {i}/{total} segments — {len(results)} intersections found")
    
    # Use spatial index to find candidates only
    candidates = list(sindex.intersection(row.geometry.bounds))
    
    for j in candidates:
        if i == j:
            continue
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
df.to_csv('/Users/snehesh/congestion_env/us_intersections.csv', index=False)
print(f"Saved {len(df)} unique intersections!")
