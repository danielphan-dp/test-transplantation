import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with empty text
    resp = app_client.post("/v1.0/json-test", data="")
    assert resp.status_code == 200
    assert resp.json() == {}

    # Test with valid JSON string
    valid_json = '{"key": "value"}'
    resp = app_client.post("/v1.0/json-test", data=valid_json, headers={"Content-Type": "application/json"})
    assert resp.status_code == 200
    assert resp.json() == json.loads(valid_json)

    # Test with invalid JSON string
    invalid_json = '{"key": "value"'
    resp = app_client.post("/v1.0/json-test", data=invalid_json, headers={"Content-Type": "application/json"})
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for bad JSON

    # Test with non-JSON data
    non_json_data = "This is not JSON"
    resp = app_client.post("/v1.0/json-test", data=non_json_data, headers={"Content-Type": "text/plain"})
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for non-JSON data

    # Test with nested JSON
    nested_json = '{"outer": {"inner": "value"}}'
    resp = app_client.post("/v1.0/json-test", data=nested_json, headers={"Content-Type": "application/json"})
    assert resp.status_code == 200
    assert resp.json() == json.loads(nested_json)