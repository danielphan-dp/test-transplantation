import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_json_method_with_valid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", json={"key": "value"})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"key": "value"}

def test_json_method_with_empty_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", json={})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {}

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", data="invalid json")
    assert response.status_code == 400
    response_data = response.json()
    assert "error" in response_data

def test_json_method_with_nested_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/json-endpoint", json={"outer": {"inner": "value"}})
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {"outer": {"inner": "value"}}