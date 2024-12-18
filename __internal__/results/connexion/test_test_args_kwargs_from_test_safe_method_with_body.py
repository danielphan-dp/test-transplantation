import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    payload = {"key": "value"}
    resp = app_client.post("/v1.0/json-endpoint", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json-endpoint", json={})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json-endpoint", data="invalid json")
    assert resp.status_code == 400

def test_json_method_with_bytes_data(simple_app):
    app_client = simple_app.test_client()
    payload = json.dumps({"key": "value"}).encode('utf-8')
    resp = app_client.post("/v1.0/json-endpoint", data=payload, content_type='application/json')
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}