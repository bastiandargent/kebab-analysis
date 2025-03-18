import json
import geopandas as gpd
import fiona



#read berlin_network.gpkg and berlin_stations.gpkg as geodataframes

berlin_network = gpd.read_file("berlin_network.gpkg", layer="edges")
berlin_stations = gpd.read_file("berlin_stations.gpkg")

# read google places api as dict

kebab_restaurants = gpd.read_file("reviews_berlin_kebab.geojson", engine="fiona")


# find the distance for every kebab restaurant's clostest train station


# evaluate the stats and if kebab restaurants are tastier the closer they are to train stations

# make graphs visualizing correlation of distance to tastiness