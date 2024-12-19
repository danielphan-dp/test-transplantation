import json
import pytest

def test_json_method_with_valid_text(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    valid_text = '{"key": "value"}'
    response = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data=valid_text
    )
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_json_method_with_empty_text(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    empty_text = ''
    response = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data=empty_text
    )
    assert response.status_code == 400

def test_json_method_with_invalid_json(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    invalid_json = '{"key": "value"'
    response = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data=invalid_json
    )
    assert response.status_code == 400

def test_json_method_with_non_json_content(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "text/plain"}
    
    non_json_text = 'This is not JSON'
    response = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data=non_json_text
    )
    assert response.status_code == 415