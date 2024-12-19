import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    valid_json = '{"key": "value"}'
    resp = app_client.post("/v1.0/json_request", data=valid_json, content_type='application/json')
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_empty_string(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json_request", data='', content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json = '{"key": "value"'
    resp = app_client.post("/v1.0/json_request", data=invalid_json, content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_unicode_characters(simple_app):
    app_client = simple_app.test_client()
    unicode_json = '{"price": "£19.99"}'
    resp = app_client.post("/v1.0/json_request", data=unicode_json, content_type='application/json')
    assert resp.status_code == 200
    assert resp.json()["price"] == "£19.99"

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    large_json = '{"data": [' + ','.join(['{"id": ' + str(i) + '}' for i in range(1000)]) + ']}'
    resp = app_client.post("/v1.0/json_request", data=large_json, content_type='application/json')
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 1000