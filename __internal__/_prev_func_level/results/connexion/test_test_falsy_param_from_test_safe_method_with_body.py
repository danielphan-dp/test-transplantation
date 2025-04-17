import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    payload = {"key": "value"}
    response = app_client.post("/v1.0/test-json-method", json=payload)
    
    assert response.status_code == 200
    assert response.json() == payload

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json-method", json={})
    
    assert response.status_code == 200
    assert response.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json-method", data="invalid json")
    
    assert response.status_code == 400
    assert "error" in response.json()

def test_json_method_with_none_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json-method", json=None)
    
    assert response.status_code == 400
    assert "error" in response.json()