import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    valid_data = '{"key": "value"}'
    resp = app_client.post("/v1.0/test-json-method", data=valid_data, content_type='application/json')
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value"}

def test_json_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    invalid_data = '{"key": "value"'
    resp = app_client.post("/v1.0/test-json-method", data=invalid_data, content_type='application/json')
    assert resp.status_code == 400
    response = resp.json()
    assert "error" in response

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    empty_data = ''
    resp = app_client.post("/v1.0/test-json-method", data=empty_data, content_type='application/json')
    assert resp.status_code == 400
    response = resp.json()
    assert "error" in response

def test_json_method_with_non_json_data(simple_app):
    app_client = simple_app.test_client()
    non_json_data = 'Just a string'
    resp = app_client.post("/v1.0/test-json-method", data=non_json_data, content_type='text/plain')
    assert resp.status_code == 400
    response = resp.json()
    assert "error" in response