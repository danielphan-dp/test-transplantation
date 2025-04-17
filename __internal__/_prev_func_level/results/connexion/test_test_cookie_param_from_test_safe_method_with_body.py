import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-json-method", data=json.dumps({"key": "value"}), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-json-method", data=json.dumps({}), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-json-method", data="invalid_json", content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-json-method", data="plain text", content_type='text/plain')
    assert response.status_code == 415

def test_json_method_with_large_data(simple_app):
    app_client = simple_app.test_client()
    large_data = json.dumps({"key": "value" * 1000})
    response = app_client.get("/v1.0/test-json-method", data=large_data, content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {"key": "value" * 1000}