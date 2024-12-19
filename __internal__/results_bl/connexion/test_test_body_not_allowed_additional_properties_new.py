import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value"}
    resp = app_client.post(
        "/v1.0/valid-json",
        json=body,
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == body

def test_json_method_with_empty_json(simple_app):
    app_client = simple_app.test_client()
    body = {}
    resp = app_client.post(
        "/v1.0/empty-json",
        json=body,
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == body

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    body = "invalid json"
    resp = app_client.post(
        "/v1.0/invalid-json",
        data=body,
    )
    assert resp.status_code == 400
    response = resp.json()
    assert "Invalid JSON" in response["detail"]

def test_json_method_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    body = {"key": None}
    resp = app_client.post(
        "/v1.0/missing-key",
        json=body,
    )
    assert resp.status_code == 400
    response = resp.json()
    assert "Key cannot be null" in response["detail"]