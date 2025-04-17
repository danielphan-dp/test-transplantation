import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    resp = app_client.get("/v1.0/test-json/valid")
    assert resp.json() == {"key": "value"}

    # Test with empty JSON string
    resp = app_client.get("/v1.0/test-json/empty")
    assert resp.json() == {}

    # Test with malformed JSON string
    resp = app_client.get("/v1.0/test-json/malformed")
    assert resp.status_code == 400

    # Test with JSON array
    resp = app_client.get("/v1.0/test-json/array")
    assert resp.json() == ["item1", "item2", "item3"]

    # Test with nested JSON
    resp = app_client.get("/v1.0/test-json/nested")
    assert resp.json() == {"outer": {"inner": "value"}}