import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_json_method_with_valid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    valid_json = '{"key": "value", "number": 123, "boolean": true}'
    
    response = app_client.post("/json-endpoint", data=valid_json, content_type='application/json')
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data == json.loads(valid_json)

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    invalid_json = '{"key": "value", "number": 123, "boolean": true'  # Missing closing brace
    
    response = app_client.post("/json-endpoint", data=invalid_json, content_type='application/json')
    assert response.status_code == 400, response.text
    response_data = response.json()
    assert "error" in response_data

def test_json_method_with_empty_string(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    empty_json = ''
    
    response = app_client.post("/json-endpoint", data=empty_json, content_type='application/json')
    assert response.status_code == 400, response.text
    response_data = response.json()
    assert "error" in response_data

def test_json_method_with_non_json_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    non_json_data = 'This is not JSON'
    
    response = app_client.post("/json-endpoint", data=non_json_data, content_type='text/plain')
    assert response.status_code == 400, response.text
    response_data = response.json()
    assert "error" in response_data

def test_json_method_with_nested_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    nested_json = '{"outer": {"inner": {"key": "value"}}}'
    
    response = app_client.post("/json-endpoint", data=nested_json, content_type='application/json')
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data == json.loads(nested_json)