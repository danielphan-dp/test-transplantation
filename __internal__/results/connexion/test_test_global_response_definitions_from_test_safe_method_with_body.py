import json
import pytest

def test_json_method_with_valid_data(schema_app):
    app_client = schema_app.test_client()
    valid_data = '{"key": "value"}'
    response = app_client.post("/v1.0/test_json", data=valid_data, content_type='application/json')
    assert response.json() == {"key": "value"}

def test_json_method_with_invalid_data(schema_app):
    app_client = schema_app.test_client()
    invalid_data = '{"key": "value"'
    response = app_client.post("/v1.0/test_json", data=invalid_data, content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_empty_data(schema_app):
    app_client = schema_app.test_client()
    empty_data = ''
    response = app_client.post("/v1.0/test_json", data=empty_data, content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_non_json_data(schema_app):
    app_client = schema_app.test_client()
    non_json_data = 'This is not JSON'
    response = app_client.post("/v1.0/test_json", data=non_json_data, content_type='text/plain')
    assert response.status_code == 400