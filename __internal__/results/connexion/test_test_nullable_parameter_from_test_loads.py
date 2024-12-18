import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    resp = app_client.post("/v1.0/json-endpoint", json={"key": "value"})
    assert resp.json() == {"key": "value"}

    # Test with empty JSON
    resp = app_client.post("/v1.0/json-endpoint", json={})
    assert resp.json() == {}

    # Test with invalid JSON
    resp = app_client.post("/v1.0/json-endpoint", data="invalid json")
    assert resp.status_code == 400

    # Test with JSON containing null
    resp = app_client.post("/v1.0/json-endpoint", json={"key": None})
    assert resp.json() == {"key": None}

    # Test with JSON containing boolean
    resp = app_client.post("/v1.0/json-endpoint", json={"key": True})
    assert resp.json() == {"key": True}

    # Test with nested JSON
    resp = app_client.post("/v1.0/json-endpoint", json={"key": {"nested_key": "nested_value"}})
    assert resp.json() == {"key": {"nested_key": "nested_value"}}