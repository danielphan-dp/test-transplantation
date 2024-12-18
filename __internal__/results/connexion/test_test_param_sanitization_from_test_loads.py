import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    resp = app_client.post(
        "/v1.0/json-test",
        json={"key": "value"},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

    # Test with empty JSON
    resp = app_client.post(
        "/v1.0/json-test",
        json={},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    assert resp.json() == {}

    # Test with invalid JSON
    resp = app_client.post(
        "/v1.0/json-test",
        data="not a json",
        headers={"Content-Type": "text/plain"},
    )
    assert resp.status_code == 400

    # Test with JSON containing nested structures
    body = {"outer": {"inner": "value"}}
    resp = app_client.post(
        "/v1.0/json-test",
        json=body,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    assert resp.json() == body

    # Test with JSON containing an array
    body = {"items": [1, 2, 3]}
    resp = app_client.post(
        "/v1.0/json-test",
        json=body,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    assert resp.json() == body

    # Test with malformed JSON
    resp = app_client.post(
        "/v1.0/json-test",
        data='{"key": "value",}',
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400

    # Test with large JSON payload
    large_body = {"key": "value" * 1000}
    resp = app_client.post(
        "/v1.0/json-test",
        json=large_body,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    assert resp.json() == large_body