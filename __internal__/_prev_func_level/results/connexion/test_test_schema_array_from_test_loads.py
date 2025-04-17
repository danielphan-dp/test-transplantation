import json
import pytest

def test_json_method(schema_app):
    app_client = schema_app.test_client()

    # Test with valid JSON string
    valid_request = app_client.post("/v1.0/json_method", json={"key": "value"})
    assert valid_request.status_code == 200
    assert valid_request.headers.get("content-type") == "application/json"
    valid_response = valid_request.json()
    assert valid_response == {"key": "value"}

    # Test with empty JSON
    empty_request = app_client.post("/v1.0/json_method", json={})
    assert empty_request.status_code == 200
    assert empty_request.headers.get("content-type") == "application/json"
    empty_response = empty_request.json()
    assert empty_response == {}

    # Test with invalid JSON
    invalid_request = app_client.post("/v1.0/json_method", data="invalid json")
    assert invalid_request.status_code == 400
    invalid_response = invalid_request.json()
    assert "error" in invalid_response

    # Test with JSON array
    array_request = app_client.post("/v1.0/json_method", json=["item1", "item2"])
    assert array_request.status_code == 200
    assert array_request.headers.get("content-type") == "application/json"
    array_response = array_request.json()
    assert array_response == ["item1", "item2"]