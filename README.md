# U.S. Highway Congestion and Density Analysis
Geometric analysis of U.S. highway congestion and intersection density using OSM road network data and INRIX 2025 Traffic Scorecard

## Overview
This project analyzes highway congestion and intersection density across the continental United States using geometric network analysis and real world congestion data from the OSM road network data.

## Methodology
1) Road Network Extraction -- Extracted 934,027 interstate and primary highway segments from OpenStreetMap via Geofabrik
2) Intersection Detection -- Used R-tree spatial indexing to identify 586,539 unique highway-to-highway intersection points across the US
3) Density Clustering —- Clustered intersections into 1km grid cells and identified the 5,000 highest-density locations
4) Voronoi Analysis —- Generated Voronoi polygons from density clusters, clipped to the continental US boundary, and calculated area-weighted density scores
5) Congestion Validation —- Overlaid INRIX 2025 busiest corridor data to validate geometric chokepoints against real-world congestion rankings

## Key Findings
1) The Northeast Corridor (Boston --> NYC --> Philadelphia --> DC) shows the highest highway intersection density in the country
2) The geometric density analysis independently corroborates INRIX 2025 findings. The Stamford, CT corridor (I-95 SB, ranked #1 nationally at 133 hours lost per driver annually) appears as one of the brightest clusters on the density map, confirming that areas of high geometric complexity consistently correspond to real-world congestion hotspots.
3) Geometric chokepoints closely match real-world congestion rankings, 
validating the network analysis approach

## Data Sources
1) Road Network: OpenStreetMap via Geofabrik (2025)
2) Congestion Data: INRIX 2025 Global Traffic Scorecard
3) US Boundary: Natural Earth

## Tools Used
1) QGIS 3.44
2) Python (GeoPandas, Shapely, osmium-tool)
3) CartoDB Dark Matter basemap
