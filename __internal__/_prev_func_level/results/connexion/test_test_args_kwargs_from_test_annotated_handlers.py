import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with empty response
    resp = app_client.get("/v1.0/empty-response")
    assert resp.status_code == 200
    assert resp.json() == {}

    # Test with valid JSON response
    resp = app_client.get("/v1.0/valid-json-response")
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

    # Test with invalid JSON response
    resp = app_client.get("/v1.0/invalid-json-response")
    assert resp.status_code == 400
    assert "error" in resp.json()

    # Test with JSON containing nested objects
    resp = app_client.get("/v1.0/nested-json-response")
    assert resp.status_code == 200
    assert resp.json() == {"outer": {"inner": "value"}}

    # Test with JSON array response
    resp = app_client.get("/v1.0/json-array-response")
    assert resp.status_code == 200
    assert resp.json() == [{"item": 1}, {"item": 2}, {"item": 3}]