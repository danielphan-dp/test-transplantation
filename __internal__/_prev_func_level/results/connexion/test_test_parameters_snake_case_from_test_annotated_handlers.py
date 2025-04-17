import json
import pytest

def test_json_method(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    
    # Test valid JSON input
    resp = app_client.post(
        "/v1.0/test-json",
        headers=headers,
        json={"key": "value"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

    # Test invalid JSON input
    resp = app_client.post(
        "/v1.0/test-json",
        headers=headers,
        data="not a json",
    )
    assert resp.status_code == 400
    assert resp.json()["detail"].startswith("Invalid JSON")

    # Test empty JSON input
    resp = app_client.post(
        "/v1.0/test-json",
        headers=headers,
        json={},
    )
    assert resp.status_code == 200
    assert resp.json() == {}

    # Test JSON with nested structure
    resp = app_client.post(
        "/v1.0/test-json",
        headers=headers,
        json={"nested": {"key": "value"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"nested": {"key": "value"}}

    # Test JSON with array
    resp = app_client.post(
        "/v1.0/test-json",
        headers=headers,
        json={"array": [1, 2, 3]},
    )
    assert resp.status_code == 200
    assert resp.json() == {"array": [1, 2, 3]}