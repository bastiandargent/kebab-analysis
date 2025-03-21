from google_places_api import format_query

def test_format_query():
    # Test input
    feature = {
        "properties": {
            "name": "Döner King",
            "addr:suburb": "Kreuzberg",
            "addr:housenumber": "42",
            "addr:street": "Oranienstr"
        }
    }
    
    # Call function
    result = format_query(feature)
    
    # Check result
    assert "Döner King" in result
    assert "Berlin" in result
    assert "Kreuzberg" in result
    assert "42" in result
    assert "Oranienstr" in result
