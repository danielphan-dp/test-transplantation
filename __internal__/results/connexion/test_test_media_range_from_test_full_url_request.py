import pytest

def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with no kwargs
    response = app_client.post("/v1.0/media_range", json={})
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with additional kwargs
    response = app_client.post("/v1.0/media_range", json={'extra': 'value'})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'extra': 'value'}

    # Test with empty json
    response = app_client.post("/v1.0/media_range", json={})
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with unexpected data type
    response = app_client.post("/v1.0/media_range", json="string_instead_of_json")
    assert response.status_code == 400  # Assuming the endpoint should return a 400 for invalid JSON

    # Test with missing required fields if applicable
    response = app_client.post("/v1.0/media_range", json={'name': None})
    assert response.status_code == 400  # Assuming the endpoint should return a 400 for invalid data