import osmnx as ox
import networkx as nx
import geopandas as gpd

# Configure OSMnx
# ox.settings.use_cache = True
# ox.settings.log_console = True

place_name = "Berlin, Germany"
# G = ox.graph_from_place(place_name, network_type="walk")

# Project the graph to UTM zone 33N (appropriate for Berlin)
# G = ox.project_graph(G, to_crs="EPSG:32633")

# Get railway stations and subway entrances
tags = {
    'railway': ['station', 'halt'],
    'tram': 'yes' 
}


stations = ox.features_from_place(place_name, tags=tags)

# Project stations to the same CRS
stations = stations.to_crs("EPSG:32633")

# Save the network and stations data
# ox.save_graph_geopackage(G, filepath='berlin_network.gpkg')
stations.to_file('berlin_stations.gpkg', driver='GPKG')

print("Analysis completed. Files saved: berlin_network.gpkg, berlin_stations.gpkg, berlin_network.png")