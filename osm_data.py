import osmnx as ox
import networkx as nx
import geopandas as gpd




def get_osm_walking_network(location):
    """Saves lcoation's walking network as gpkg in project's folder."""

    walk_graph = ox.graph_from_place(location, network_type="walk")
    walk_graph = ox.project_graph(walk_graph, to_crs="EPSG:32633")
    ox.save_graph_geopackage(walk_graph, filepath='berlin_network.gpkg')
    print("Analysis completed. File save: berlin_network.gpkg")



def get_osm_train_station(location):
    """Saves location's train stations (station, halt, tram) as gpkg in project's folder."""
    tags = {
        'railway': ['station', 'halt'],
        'tram': 'yes' 
    }
    stations = ox.features_from_place(location, tags=tags)
    stations = stations.to_crs("EPSG:32633")
    stations.to_file('berlin_stations.gpkg', driver='GPKG')
    print("Analysis completed. File save: berlin_stations.gpkg")



