import json
import pytest

def test_json_method_with_valid_json(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-json-valid",
        headers=headers,
        json={"key": "value"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_json(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-json-empty",
        headers=headers,
        json={},
    )
    assert resp.status_code == 200
    assert resp.json() == {}

def test_json_method_with_invalid_json(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-json-invalid",
        headers=headers,
        data="not a json",
    )
    assert resp.status_code == 400
    assert resp.json()["detail"].startswith("Invalid JSON")

def test_json_method_with_nested_json(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-json-nested",
        headers=headers,
        json={"outer": {"inner": "value"}},
    )
    assert resp.status_code == 200
    assert resp.json() == {"outer": {"inner": "value"}} 

def test_json_method_with_large_json(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    large_json = {"key": "value" * 1000}
    resp = app_client.post(
        "/v1.0/test-json-large",
        headers=headers,
        json=large_json,
    )
    assert resp.status_code == 200
    assert resp.json() == large_json

def test_json_method_with_special_characters(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-json-special",
        headers=headers,
        json={"key": "!@#$%^&*()"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"key": "!@#$%^&*()"}