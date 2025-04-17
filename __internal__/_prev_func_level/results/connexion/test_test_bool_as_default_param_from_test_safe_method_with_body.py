import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    valid_json = '{"key": "value"}'
    response = app_client.post("/v1.0/test-json", data=valid_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"key": "value"}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json = '{"key": "value"'
    response = app_client.post("/v1.0/test-json", data=invalid_json, content_type='application/json')
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"].startswith("Expecting value")

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json", data='', content_type='application/json')
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"] == "No JSON object could be decoded"

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-json", data='Not a JSON', content_type='text/plain')
    assert response.status_code == 400
    response_data = response.json()
    assert response_data["detail"].startswith("Expecting value")