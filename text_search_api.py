import requests
import json
import asyncio
import aiohttp


API_KEY = "AIzaSyDqSE_mOTEmzyN36mp9Wd9L9wYenYaHoMQ"  
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

            # Geometry Type of restaurants can be either Polygon or Point
            location = extract_location(feature)

            payload = build_payload(query, location)

            result.append(fetch_data(session, payload))
        
        # Wait for all the API calls to finish concurrently
        return await asyncio.gather(*result)


# Serialize
def write_result(result_json):  # creates a json file with the results of the search
    with open("result.geojson", "a", encoding="utf-8") as file:
        json.dump(result_json, file)


# Main execution
async def main():
    kebabs_berlin = read_json()

    result = await search_text(kebabs_berlin)

    write_result(result)

# Run the async main function
asyncio.run(main())


# test first entry
# result = search_text(
# {
#   "type": "FeatureCollection",
#   "generator": "overpass-turbo",
#   "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.",
#   "timestamp": "2025-03-04T18:09:26Z",
#   "features": [
#     {
#       "type": "Feature",
#       "properties": {
#         "@id": "way/40748388",
#         "addr:city": "Berlin",
#         "addr:country": "DE",
#         "addr:housenumber": "165",
#         "addr:street": "Sonnenallee",
#         "addr:suburb": "Neukölln",
#         "amenity": "fast_food",
#         "building": "kiosk",
#         "building:levels": "1",
#         "cuisine": "kebab",
#         "name": "Traum Eck",
#         "wheelchair": "no"
#       },
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [
#           [
#             [13.448244, 52.4778619],
#             [13.4483551, 52.4778078],
#             [13.448429, 52.4778638],
#             [13.4483184, 52.4779183],
#             [13.448244, 52.4778619]
#           ]
#         ]
#       },
#       "id": "way/40748388"
#     }
#   ]
# }  
# )

# write_result(result)

