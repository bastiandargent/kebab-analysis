import pytest
from unittest.mock import patch
from text_search_api import search_text

# Test data with Polygon geometry
test_geojson_polygon = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "name": "Traum Eck",
            "addr:suburb": "Neukölln",
            "addr:housenumber": "165",
            "addr:street": "Sonnenallee"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [13.448244, 52.4778619],
                [13.4483551, 52.4778078],
                [13.448429, 52.4778638],
                [13.4483184, 52.4779183],
                [13.448244, 52.4778619]
            ]]
        }
    }]
}

# Test data with Point geometry
test_geojson_point = {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "name": "Test Kebab",
            "addr:suburb": "Mitte",
            "addr:housenumber": "1",
            "addr:street": "Test Street"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [13.448244, 52.4778619]
        }
    }]
}

# Mock API response
mock_api_response = {
    "places": [{
        "displayName": {
            "text": "Traum Eck"
        },
        "rating": 4.5,
        "userRatingCount": 100
    }]
}

@pytest.mark.parametrize("test_input,expected_coordinates", [
    (test_geojson_polygon, {"latitude": 52.4778619, "longitude": 13.448244}),
    (test_geojson_point, {"latitude": 52.4778619, "longitude": 13.448244})
])
@patch('requests.post')
def test_search_text(mock_post, test_input, expected_coordinates):
    # Configure mock
    mock_post.return_value.json.return_value = mock_api_response
    mock_post.return_value.status_code = 200

    # Call the function
    result = search_text(test_input)

    # Assertions
    assert len(result) == 1  # One feature should produce one result
    assert result[0] == mock_api_response  # Check if response matches mock

    # Verify the API was called with correct parameters
    called_args = mock_post.call_args[1]
    
    # Check if payload contains correct location
    assert called_args['json']['locationBias']['circle']['center'] == expected_coordinates
    assert called_args['json']['locationBias']['circle']['radius'] == 100.0

    # Verify expected query format
    feature = test_input['features'][0]
    expected_query = f"{feature['properties']['name']} \
            Berlin \
            {feature['properties']['addr:suburb']} \
            {feature['properties']['addr:housenumber']} \
            {feature['properties']['addr:street']}"
    assert called_args['json']['textQuery'] == expected_query
