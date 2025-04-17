import json
import pytest

def test_json(simple_app):
    app_client = simple_app.test_client()

    # Test with valid JSON string
    valid_json_response = app_client.post("/v1.0/json", data=json.dumps({"key": "value"}), content_type='application/json')
    assert valid_json_response.status_code == 200
    assert valid_json_response.json() == {"key": "value"}

    # Test with invalid JSON string
    invalid_json_response = app_client.post("/v1.0/json", data="invalid json", content_type='application/json')
    assert invalid_json_response.status_code == 400
    assert "error" in invalid_json_response.json()

    # Test with empty JSON
    empty_json_response = app_client.post("/v1.0/json", data=json.dumps({}), content_type='application/json')
    assert empty_json_response.status_code == 200
    assert empty_json_response.json() == {}

    # Test with JSON containing special characters
    special_char_json_response = app_client.post("/v1.0/json", data=json.dumps({"message": "Hello, world!"}), content_type='application/json')
    assert special_char_json_response.status_code == 200
    assert special_char_json_response.json() == {"message": "Hello, world!"}

    # Test with JSON array
    json_array_response = app_client.post("/v1.0/json", data=json.dumps([1, 2, 3]), content_type='application/json')
    assert json_array_response.status_code == 200
    assert json_array_response.json() == [1, 2, 3]