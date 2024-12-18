import json
import pytest
from io import BytesIO

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    payload = {"key": "value"}
    response = app_client.post(
        "/v1.0/test-json-method",
        json=payload
    )
    assert response.status_code == 200
    assert response.json() == payload

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post(
        "/v1.0/test-json-method",
        json={}
    )
    assert response.status_code == 200
    assert response.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post(
        "/v1.0/test-json-method",
        data="invalid json"
    )
    assert response.status_code == 400

def test_json_method_with_large_data(simple_app):
    app_client = simple_app.test_client()
    large_payload = {f"key{i}": f"value{i}" for i in range(1000)}
    response = app_client.post(
        "/v1.0/test-json-method",
        json=large_payload
    )
    assert response.status_code == 200
    assert response.json() == large_payload

def test_json_method_with_nested_json(simple_app):
    app_client = simple_app.test_client()
    nested_payload = {"outer": {"inner": "value"}}
    response = app_client.post(
        "/v1.0/test-json-method",
        json=nested_payload
    )
    assert response.status_code == 200
    assert response.json() == nested_payload