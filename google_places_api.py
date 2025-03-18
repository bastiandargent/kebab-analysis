import json
import asyncio
import aiohttp
from dotenv import load_dotenv
import os

load_dotenv()


API_KEY = os.getenv("GOOGLE_API_KEY")
URL = "https://places.googleapis.com/v1/places:searchText"

headers = {
    "Content-Type":"application/json",
    "X-Goog-Api-Key":API_KEY,
    "X-Goog-FieldMask":"places.displayName,places.rating,places.userRatingCount",
}


def format_query(feature):
    return f'{feature["properties"].get("name","")} \
            Berlin \
            {feature["properties"].get("addr:suburb","")} \
            {feature["properties"].get("addr:housenumber","")} \
            {feature["properties"].get("addr:street","")}'

def extract_location(feature):
    """Extraction of kebab restaurant coordinates"""
    geometry_type = feature["geometry"]["type"]
    if geometry_type == "Polygon":

        return {"latitude": feature["geometry"]["coordinates"][0][0][1], "longitude": feature["geometry"]["coordinates"][0][0][0]}

    elif geometry_type == "Point":
        return {"latitude": feature["geometry"]["coordinates"][1], "longitude": feature["geometry"]["coordinates"][0]}

    else:
        return {}
    

def build_payload(query, location):
    return {
            "textQuery": query,
            "locationBias": {
                "circle": {
                    "center": location,
                    "radius": 100.0,
                }
            }
        }

    
# converts json to dict
def read_json():
    with open("berlin_kebab.geojson", "r", encoding="utf-8") as file:
        geojson_file = json.load(file)
    return geojson_file


async def fetch_data(session, payload):
    async with session.post(URL, headers=headers, json=payload) as response:
        return await response.json()

# calls Google Search Text API
async def search_text(json_input):

    result = []

    async with aiohttp.ClientSession() as session:
        for feature in json_input["features"]:
          
            query = format_query(feature)

            location = extract_location(feature)

            payload = build_payload(query, location)

            result.append(fetch_data(session, payload))
        
        # Wait for all the API calls to finish concurrently
        return await asyncio.gather(*result)



def write_result(result):
    """Serialize google places restaurant results into geojson format."""
    with open("reviews_berlin_kebab.geojson", "w", encoding="utf-8") as reviews_file:
        ratings = []
        userRatingCounts = []


        for entry in result:
            try:
                ratings.append(entry["places"][0]["rating"])
            except (KeyError):
                ratings.append(None)

        for entry in result:
            try:
                userRatingCounts.append(entry["places"][0]["userRatingCount"])
            except (KeyError):
                userRatingCounts.append(None)

        osm_geojson = read_json()
        features = osm_geojson["features"]

        for feature, rating, userRatingCount in zip(features, ratings, userRatingCounts):
            feature["properties"]["rating"] = rating
            feature["properties"]["userRatingCount"] = userRatingCount

        json.dump(osm_geojson, reviews_file)


