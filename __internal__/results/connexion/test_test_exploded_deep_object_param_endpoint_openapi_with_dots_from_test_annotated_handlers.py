import json
import pytest

def test_json_method_with_valid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/test-json", json={"key": "value"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"key": "value"}

def test_json_method_with_empty_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/test-json", json={})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/test-json", data="invalid json")
    assert response.status_code == 400

def test_json_method_with_nested_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/test-json", json={"outer": {"inner": "value"}})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"outer": {"inner": "value"}}