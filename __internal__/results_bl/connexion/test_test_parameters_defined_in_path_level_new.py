import json
import io.BytesIO
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    valid_json_response = '{"key": "value"}'
    resp = app_client.post("/v1.0/json-endpoint", data=valid_json_response, content_type='application/json')
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json_response = '{"key": "value"'
    resp = app_client.post("/v1.0/json-endpoint", data=invalid_json_response, content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/json-endpoint", data='', content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    non_json_response = 'Just a string'
    resp = app_client.post("/v1.0/json-endpoint", data=non_json_response, content_type='text/plain')
    assert resp.status_code == 400

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    large_json_response = json.dumps({"key": "value" * 1000})
    resp = app_client.post("/v1.0/json-endpoint", data=large_json_response, content_type='application/json')
    assert resp.status_code == 200
    assert resp.json() == {"key": "value" * 1000}