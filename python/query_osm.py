# to be run on a machine with high memory 

from pyrosm import OSM
from pyrosm import get_data
import pandas as pd
import geopandas as gpd
import json

print("=====getting data")
fp = get_data("england")
osm = OSM(fp)

print("====getting pois")
custom_filter = {'amenity': True, 'shop': True} 
pois = osm.get_pois(custom_filter=custom_filter)

print("====gathering info about pois type")
# Gather info about POI type (combines the tag info from "amenity" and "shop")
pois["poi_type"] = pois["amenity"]
pois["poi_type"] = pois["poi_type"].fillna(pois["shop"])


# Filter charities
charities_osm = pois.loc[pois['poi_type']=='charity']

# Choose columns
charity_filtered = charities_osm[['lat', 'lon', 'name','tags', 'geometry']]

# Filter all None values
charity_filtered = charity_filtered[charity_filtered['tags'].notnull()]

# Reset indices
charity_filtered = charity_filtered.reset_index()



## Create a df with charities without tags in order to join two df later

# Filter all values without tags
charity_notags = charities_osm[charities_osm['tags'].isnull()]

# Choose columns
charity_notags = charity_notags[['lat', 'lon', 'name','tags', 'geometry']]




# Convert string 'tags' to JSON objects
charity_filtered["tags"] = charity_filtered["tags"].apply(json.loads)

# Convert JSON 'tags' to columns
charity_tags = pd.json_normalize(charity_filtered["tags"])

# Choose columns
charity_tags_filtered = charity_tags[['brand', 'brand:wikidata', 'addr:suburb']] # brand:wikidata is a unique code for shops/chains in osm world

# Join tags with df
charity_joined = pd.concat([charity_filtered, charity_tags_filtered], axis=1)

# Without None values in brand, wikidata and suburb -> this should filter all the odd datapoints, but some duplicates can still exist
charity_joined_filtered = charity_joined[charity_joined['brand'].notnull() |
                                             charity_joined['brand:wikidata'].notnull() |
                                             charity_joined['addr:suburb'].notnull()]

# Join two df (with tags and no tags)

charities = pd.concat([charity_joined_filtered, charity_notags])


# Convert polygons to points

charity_points = charities.copy()

# Change geometry 
charity_points['geometry'] = charity_points['geometry'].centroid



# Convert points into lat, lon coordinate
charity_coords = charity_points.copy()

charity_coords['lon'] = charity_coords.geometry.x
charity_coords['lat'] = charity_coords.geometry.y


charity_coords.to_csv('charity_coords_OSM_raw.csv')

