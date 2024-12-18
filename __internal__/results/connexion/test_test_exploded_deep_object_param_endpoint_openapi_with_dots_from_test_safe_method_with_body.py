import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_json_method_with_valid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    valid_json = '{"key": "value"}'
    response = app_client.post("/v1.0/json-endpoint", data=valid_json, content_type='application/json')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"key": "value"}

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    invalid_json = '{"key": "value"'
    response = app_client.post("/v1.0/json-endpoint", data=invalid_json, content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_empty_body(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", data='', content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_non_json_content(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", data='plain text', content_type='text/plain')
    assert response.status_code == 415

def test_json_method_with_nested_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    nested_json = '{"outer": {"inner": "value"}}'
    response = app_client.post("/v1.0/json-endpoint", data=nested_json, content_type='application/json')
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"outer": {"inner": "value"}}