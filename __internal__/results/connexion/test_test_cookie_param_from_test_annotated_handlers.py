import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    response = app_client.post("/v1.0/json-endpoint", data=json.dumps({"key": "value"}), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

    # Test with invalid JSON string
    response = app_client.post("/v1.0/json-endpoint", data="invalid json", content_type='application/json')
    assert response.status_code == 400

    # Test with empty JSON
    response = app_client.post("/v1.0/json-endpoint", data=json.dumps({}), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {}

    # Test with JSON containing different data types
    response = app_client.post("/v1.0/json-endpoint", data=json.dumps({"int": 1, "float": 1.5, "str": "test", "list": [1, 2, 3]}), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {"int": 1, "float": 1.5, "str": "test", "list": [1, 2, 3]}