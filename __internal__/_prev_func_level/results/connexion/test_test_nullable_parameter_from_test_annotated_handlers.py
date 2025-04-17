import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    resp = app_client.post("/v1.0/json-endpoint", data=json.dumps({"key": "value"}), headers={"Content-Type": "application/json"})
    assert resp.json() == {"key": "value"}

    # Test with empty JSON
    resp = app_client.post("/v1.0/json-endpoint", data=json.dumps({}), headers={"Content-Type": "application/json"})
    assert resp.json() == {}

    # Test with invalid JSON
    resp = app_client.post("/v1.0/json-endpoint", data="not a json", headers={"Content-Type": "application/json"})
    assert resp.status_code == 400

    # Test with None value
    resp = app_client.post("/v1.0/json-endpoint", data=json.dumps({"key": None}), headers={"Content-Type": "application/json"})
    assert resp.json() == {"key": None}

    # Test with nested JSON
    resp = app_client.post("/v1.0/json-endpoint", data=json.dumps({"nested": {"key": "value"}}), headers={"Content-Type": "application/json"})
    assert resp.json() == {"nested": {"key": "value"}}