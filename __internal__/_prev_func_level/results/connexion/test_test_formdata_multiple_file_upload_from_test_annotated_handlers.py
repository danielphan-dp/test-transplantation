import json
import pytest
from io import BytesIO

def test_json_method_with_valid_input(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data=json.dumps({"key": "value"}),
        content_type='application/json'
    )
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_input(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data=json.dumps({}),
        content_type='application/json'
    )
    assert resp.status_code == 200
    assert resp.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data="invalid json",
        content_type='application/json'
    )
    assert resp.status_code == 400
    assert "error" in resp.json()

def test_json_method_with_large_input(simple_app):
    app_client = simple_app.test_client()
    large_data = {f"key{i}": f"value{i}" for i in range(1000)}
    resp = app_client.post(
        "/v1.0/test-json-method",
        data=json.dumps(large_data),
        content_type='application/json'
    )
    assert resp.status_code == 200
    assert resp.json() == large_data

def test_json_method_with_nested_json(simple_app):
    app_client = simple_app.test_client()
    nested_data = {"outer": {"inner": "value"}}
    resp = app_client.post(
        "/v1.0/test-json-method",
        data=json.dumps(nested_data),
        content_type='application/json'
    )
    assert resp.status_code == 200
    assert resp.json() == nested_data