import json
import pytest
from io import BytesIO

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-json-method",
        data=json.dumps({"key": "value"}),
        content_type='application/json'
    )
    assert resp.status_code == 200
    assert resp.json == {"key": "value"}

def test_json_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-json-method",
        data="invalid json",
        content_type='application/json'
    )
    assert resp.status_code == 400

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-json-method",
        data=json.dumps({}),
        content_type='application/json'
    )
    assert resp.status_code == 200
    assert resp.json == {}

def test_json_method_with_large_data(simple_app):
    app_client = simple_app.test_client()
    
    large_data = {"key": "value" * 1000}
    resp = app_client.post(
        "/v1.0/test-json-method",
        data=json.dumps(large_data),
        content_type='application/json'
    )
    assert resp.status_code == 200
    assert resp.json == large_data

def test_json_method_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.post(
        "/v1.0/test-json-method",
        data=json.dumps({"missing_key": None}),
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert "missing_key" in resp.json.get("errors", [])