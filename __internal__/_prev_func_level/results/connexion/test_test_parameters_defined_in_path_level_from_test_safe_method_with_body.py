import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    payload = {"key": "value"}
    response = app_client.post("/v1.0/json-endpoint", json=payload)
    
    assert response.status_code == 200
    assert response.json() == payload

def test_json_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", data="invalid json")
    
    assert response.status_code == 400

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", json={})
    
    assert response.status_code == 200
    assert response.json() == {}

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", data="text/plain")
    
    assert response.status_code == 400

def test_json_method_with_large_data(simple_app):
    app_client = simple_app.test_client()
    payload = {"key": "value" * 1000}
    response = app_client.post("/v1.0/json-endpoint", json=payload)
    
    assert response.status_code == 200
    assert response.json() == payload