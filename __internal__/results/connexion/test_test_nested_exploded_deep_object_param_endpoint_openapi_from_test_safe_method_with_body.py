import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_json_method_with_valid_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    payload = {"key": "value"}
    response = app_client.post("/v1.0/test-json", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == payload

def test_json_method_with_empty_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/test-json", json={})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/test-json", data="invalid json")
    assert response.status_code == 400

def test_json_method_with_nested_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    payload = {"outer": {"inner": "value"}}
    response = app_client.post("/v1.0/test-json", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == payload

def test_json_method_with_large_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    payload = {"large": "x" * 10000}
    response = app_client.post("/v1.0/test-json", json=payload)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == payload