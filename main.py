import asyncio
import json    
from osm_data import get_osm_walking_network, get_osm_train_station
from google_places_api import search_text, read_json, write_result



async def main():


    location = "Berlin, Germany"
    get_osm_walking_network(location)
    get_osm_train_station(location)

    kebabs_berlin = read_json()
    # If statement checks if result exists then skip api and directly write the result

    result = await search_text(kebabs_berlin)
    write_result(result)



if __name__ == "__main__":
    asyncio.run(main())

