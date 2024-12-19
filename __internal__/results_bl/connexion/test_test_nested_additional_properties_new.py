import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_json_method_with_empty_string(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data='',
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400

def test_json_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data='{"invalid_json": True,}',
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400

def test_json_method_with_valid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        json={"valid": True},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"valid": True}

def test_json_method_with_nested_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        json={"nested": {"key": "value"}},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"nested": {"key": "value"}}