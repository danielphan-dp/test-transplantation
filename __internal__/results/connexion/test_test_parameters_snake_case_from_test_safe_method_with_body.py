import json
import pytest

def test_json_method_with_valid_data(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-json-method",
        headers=headers,
        json={"key": "value"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_data(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-json-method",
        headers=headers,
        json={},
    )
    assert resp.status_code == 200
    assert resp.json() == {}

def test_json_method_with_invalid_json(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-json-method",
        headers=headers,
        data="invalid json",
    )
    assert resp.status_code == 400
    assert resp.json()["detail"].startswith("Invalid JSON")

def test_json_method_with_non_json_content(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "text/plain"}
    resp = app_client.post(
        "/v1.0/test-json-method",
        headers=headers,
        data="Just a plain text",
    )
    assert resp.status_code == 415
    assert resp.json()["detail"] == "Unsupported Media Type"

def test_json_method_with_large_data(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    large_data = {"key": "value" * 10000}
    resp = app_client.post(
        "/v1.0/test-json-method",
        headers=headers,
        json=large_data,
    )
    assert resp.status_code == 200
    assert resp.json() == large_data