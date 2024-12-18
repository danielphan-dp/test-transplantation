import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value"}
    resp = app_client.post("/v1.0/test-json", json=body)
    assert resp.status_code == 200
    response_data = resp.json()
    assert response_data == body

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    body = "{invalid_json}"
    resp = app_client.post("/v1.0/test-json", data=body)
    assert resp.status_code == 400
    response_data = resp.json()
    assert "Invalid JSON" in response_data["detail"]

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", json={})
    assert resp.status_code == 200
    response_data = resp.json()
    assert response_data == {}

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value" * 1000}
    resp = app_client.post("/v1.0/test-json", json=body)
    assert resp.status_code == 200
    response_data = resp.json()
    assert response_data == body

def test_json_method_with_special_characters(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "!@#$%^&*()"}
    resp = app_client.post("/v1.0/test-json", json=body)
    assert resp.status_code == 200
    response_data = resp.json()
    assert response_data == body