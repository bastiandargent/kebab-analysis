import requests
import json

API_KEY = "AIzaSyDqSE_mOTEmzyN36mp9Wd9L9wYenYaHoMQ"  # Replace with your API key
URL = "https://places.googleapis.com/v1/places:searchNearby"

# headers = {
#     "Content-Type": "application/json",
#     "X-Goog-Api-Key": API_KEY,
#     "X-Goog-FieldMask": "places.displayName,places.rating,places.userRatingCount"
# }

# payload = {
#     "includedTypes": ["restaurant"],
#     "maxResultCount": 10,
#     "locationRestriction": {
#         "circle": {
#             "center": {"latitude": 37.7937, "longitude": -122.3965},
#             "radius": 500.0
#         }
#     }
# }

# response = requests.post(URL, headers=headers, json=payload)

# # Print results
# print(response.status_code, response.reason)
# print(json.dumps(response.json(), indent=2))


# # print(result)


