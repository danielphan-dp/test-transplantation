import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json", data=json.dumps({"key": "value"}), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_json_method_with_empty_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json", data=json.dumps({}), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json", data="invalid json", content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_missing_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json", data=None, content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    large_data = {"key": "value" * 10000}
    response = app_client.post("/v1.0/test-json", data=json.dumps(large_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json() == large_data