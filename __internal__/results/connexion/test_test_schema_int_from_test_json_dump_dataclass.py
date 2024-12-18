import json
import pytest

def test_json_method(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    # Test with valid JSON string
    valid_json_request = app_client.post("/v1.0/schema_int", json='{"key": "value"}')
    assert valid_json_request.status_code == 200
    assert valid_json_request.headers.get("content-type") == "application/json"
    valid_json_response = valid_json_request.json()
    assert valid_json_response == {"key": "value"}

    # Test with empty JSON
    empty_json_request = app_client.post("/v1.0/schema_int", json={})
    assert empty_json_request.status_code == 200
    assert empty_json_request.headers.get("content-type") == "application/json"
    empty_json_response = empty_json_request.json()
    assert empty_json_response == {}

    # Test with invalid JSON
    invalid_json_request = app_client.post("/v1.0/schema_int", json='invalid_json')
    assert invalid_json_request.status_code == 400  # Assuming 400 for bad request
    assert invalid_json_request.headers.get("content-type") == "application/json"
    invalid_json_response = invalid_json_request.json()
    assert "error" in invalid_json_response  # Assuming the response contains an error key

    # Test with nested JSON
    nested_json_request = app_client.post("/v1.0/schema_int", json={"outer": {"inner": 42}})
    assert nested_json_request.status_code == 200
    assert nested_json_request.headers.get("content-type") == "application/json"
    nested_json_response = nested_json_request.json()
    assert nested_json_response == {"outer": {"inner": 42}}