import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json_method", json={"key": "value"})
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json_method", json={})
    assert resp.status_code == 200
    assert resp.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json_method", data="not a json")
    assert resp.status_code == 400

def test_json_method_with_unicode(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json_method", json={"price": "£19.99"})
    assert resp.status_code == 200
    assert resp.json()["price"] == "£19.99"

def test_json_method_with_nested_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json_method", json={"data": {"key": "value"}})
    assert resp.status_code == 200
    assert resp.json() == {"data": {"key": "value"}}