import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json-method", json={"key": "value"})
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json-method", json={})
    assert resp.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json-method", data="invalid_json")
    assert resp.status_code == 400

def test_json_method_with_nested_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json-method", json={"nested": {"key": "value"}})
    assert resp.json() == {"nested": {"key": "value"}}