import requests
import json

API_KEY = "AIzaSyDqSE_mOTEmzyN36mp9Wd9L9wYenYaHoMQ"  # Replace with your API key
URL = "https://places.googleapis.com/v1/places:searchText"

headers = {
    "Content-Type":"application/json",
    "X-Goog-Api-Key":API_KEY,
    "X-Goog-FieldMask":"places.displayName,places.rating,places.userRatingCount",
}



    
# converts json to dict
def read_json():
    with open("berlin_kebab.geojson", "r", encoding="utf-8") as file:
        geojson_file = json.load(file)
    return geojson_file


# extracts payload from input and calls Google Search Text API
def search_text(json_input):

    result = []

    for feature in json_input["features"]:
        query = feature["properties"].get("name","")+" "+ \
                "Berlin" +" "+ \
                feature["properties"].get("addr:suburb","")+" "+ \
                feature["properties"].get("addr:housenumber","")+" "+ \
                feature["properties"].get("addr:street","")
        

        # Geometry Type of restaurants can be either Poylgon or Point
        geometry_type = feature["geometry"]["type"]
        if geometry_type == "Polygon":

            location = {
                
                "latitude": feature["geometry"]["coordinates"][0][0][1], 
                "longitude": feature["geometry"]["coordinates"][0][0][0]
                }

        elif geometry_type == "Point":
            location = {
                "latitude": feature["geometry"]["coordinates"][1], 
                "longitude": feature["geometry"]["coordinates"][0]
                }

        else:
            location = {}

        payload = {
            "textQuery": query,
            "locationBias": {
                "circle": {
                    "center": location,
                    "radius": 100.0,
                }
            }
        }

        response = requests.post(URL, headers=headers, json=payload)
        result.append(response.json())

    return result

# Serialize
def write_result(result_json): # creates a json file with the results of the search
    with open("result.geojson", "w", encoding="utf-8") as file:
        json.dump(result_json, file)



kebabs_berlin = read_json()

result = search_text(
{
  "type": "FeatureCollection",
  "generator": "overpass-turbo",
  "copyright": "The data included in this document is from www.openstreetmap.org. The data is made available under ODbL.",
  "timestamp": "2025-03-04T18:09:26Z",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "@id": "way/40748388",
        "addr:city": "Berlin",
        "addr:country": "DE",
        "addr:housenumber": "165",
        "addr:street": "Sonnenallee",
        "addr:suburb": "Neukölln",
        "amenity": "fast_food",
        "building": "kiosk",
        "building:levels": "1",
        "cuisine": "kebab",
        "name": "Traum Eck",
        "wheelchair": "no"
      },
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [
            [13.448244, 52.4778619],
            [13.4483551, 52.4778078],
            [13.448429, 52.4778638],
            [13.4483184, 52.4779183],
            [13.448244, 52.4778619]
          ]
        ]
      },
      "id": "way/40748388"
    }
  ]
}  
)

# result = search_text(kebabs_berlin)
print(result)


# write_result(result)