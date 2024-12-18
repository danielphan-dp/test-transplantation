import pytest

def test_post_method(schema_app):
    app_client = schema_app.test_client()

    # Test with valid input
    valid_input = {"key": "value"}
    response = app_client.post("/v1.0/post_method", json=valid_input)
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

    # Test with empty input
    empty_input = {}
    response = app_client.post("/v1.0/post_method", json=empty_input)
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

    # Test with invalid input type
    invalid_input = "invalid_string"
    response = app_client.post("/v1.0/post_method", json=invalid_input)
    assert response.status_code == 400
    assert response.headers.get("content-type") == "application/problem+json"
    invalid_response = response.json()
    assert invalid_response["title"] == "Bad Request"
    assert invalid_response["detail"].startswith("invalid_string is not of type 'object'")

    # Test with unexpected key
    unexpected_key_input = {"unexpected_key": "value"}
    response = app_client.post("/v1.0/post_method", json=unexpected_key_input)
    assert response.status_code == 201
    assert response.json() == {"unexpected_key": "value", "name": "post"}