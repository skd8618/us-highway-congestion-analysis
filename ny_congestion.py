# ny_congestion.py
# Builds a dataset of the busiest highway corridors in the Northeast US
# using real data from the INRIX 2025 Global Traffic Scorecard (Page 19).
# Corridors are classified by severity based on annual hours lost per driver.
# Output: ny_chokepoints.csv -- used as a point layer in QGIS

import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data pulled directly from INRIX 2025 Global Traffic Scorecard, Page 19
# Only Northeast Corridor entries are included (CT, NY, MA, PA, MD, DC)
corridors = {
    'name': [
        'I-95 SB Stamford CT',
        'I-95 NB Stamford CT',
        'I-278 WB Brooklyn-Queens Expy NY',
        'I-93 SB Boston MA',
        'I-495 CCW Capital Beltway DC',
        'Anacostia Fwy NB DC',
        'I-95 SB Philadelphia PA',
        'I-93 NB Boston MA',
        'I-95 NB Philadelphia PA',
        'I-278 EB Brooklyn-Queens Expy NY',
        'I-95 SB New Haven CT',
        'I-95 NB Bridgeport CT',
        'I-270 SB Rockville MD',
        'I-66 EB Washington DC',
        'I-76 EB Schuylkill Expy Philadelphia',
    ],
    'road': [
        'I-95','I-95','I-278','I-93','I-495',
        'Anacostia Fwy','I-95','I-93','I-95','I-278',
        'I-95','I-95','I-270','I-66','I-76',
    ],
    'state': [
        'CT','CT','NY','MA','DC',
        'DC','PA','MA','PA','NY',
        'CT','CT','MD','DC','PA',
    ],
    'city': [
        'Stamford','Stamford','New York City','Boston','Washington DC',
        'Washington DC','Philadelphia','Boston','Philadelphia','New York City',
        'New Haven','Bridgeport','Rockville','Washington DC','Philadelphia',
    ],
    'direction': [
        'SB','NB','WB','SB','CCW',
        'NB','SB','NB','NB','EB',
        'SB','NB','SB','EB','EB',
    ],
    'peak_hour': [
        '8:00 AM','5:00 PM','4:00 PM','3:00 PM','4:00 PM',
        '4:00 PM','8:00 AM','5:00 PM','5:00 PM','4:00 PM',
        '5:00 PM','5:00 PM','8:00 AM','8:00 AM','8:00 AM',
    ],
    'peak_type': [
        'AM','PM','PM','PM','PM',
        'PM','AM','PM','AM','PM',
        'PM','PM','AM','AM','AM',
    ],
    # Hours lost per driver annually at peak hour — INRIX 2025, Page 19
    'hours_lost': [
        133, 94, 93, 81, 64,
        63, 58, 55, 52, 49,
        47, 89, 44, 41, 38,
    ],
    # National rank from INRIX 2025 Top 25 Busiest Corridors list
    'inrix_us_rank': [
        1, 2, 3, 8, 21,
        22, None, None, None, None,
        None, 6, None, None, None,
    ],
    'lat': [
        41.053, 41.053, 40.678, 42.361, 38.978,
        38.868, 39.952, 42.361, 39.952, 40.678,
        41.308, 41.186, 39.084, 38.889, 39.965,
    ],
    'lon': [
        -73.541, -73.541, -73.990, -71.060, -77.015,
        -77.050, -75.143, -71.060, -75.143, -73.990,
        -72.928, -73.195, -77.147, -77.107, -75.181,
    ],
    'source': ['INRIX 2025 Global Traffic Scorecard'] * 15,
}

df = pd.DataFrame(corridors)

# Classify corridors by severity based on hours lost annually
def severity(hours):
    if hours >= 90: return 'Severe'
    elif hours >= 60: return 'High'
    elif hours >= 40: return 'Moderate'
    else: return 'Low'

df['severity'] = df['hours_lost'].apply(severity)

df.to_csv(os.path.join(BASE_DIR, 'ny_chokepoints.csv'), index=False)
print(f"Done! {len(df)} corridors saved.")
print(df[['name', 'peak_hour', 'hours_lost', 'severity']].to_string())
