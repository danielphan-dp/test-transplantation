import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    valid_json = '{"key": "value"}'
    resp = app_client.post("/v1.0/json-test", data=valid_json, headers={"Content-Type": "application/json"})
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

    # Test with invalid JSON string
    invalid_json = '{"key": "value"'
    resp = app_client.post("/v1.0/json-test", data=invalid_json, headers={"Content-Type": "application/json"})
    assert resp.status_code == 400

    # Test with empty JSON
    empty_json = '{}'
    resp = app_client.post("/v1.0/json-test", data=empty_json, headers={"Content-Type": "application/json"})
    assert resp.status_code == 200
    assert resp.json() == {}

    # Test with JSON containing different data types
    complex_json = '{"string": "text", "number": 123, "boolean": true, "null_value": null}'
    resp = app_client.post("/v1.0/json-test", data=complex_json, headers={"Content-Type": "application/json"})
    assert resp.status_code == 200
    assert resp.json() == {
        "string": "text",
        "number": 123,
        "boolean": True,
        "null_value": None
    }