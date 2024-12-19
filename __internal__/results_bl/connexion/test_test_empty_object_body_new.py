import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_json_with_empty_string(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-with-empty-string",
        data='',
    )
    assert resp.status_code == 400

def test_json_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-with-invalid-json",
        data='{"invalid":}',
    )
    assert resp.status_code == 400

def test_json_with_non_json_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-with-non-json-data",
        data='This is not JSON',
    )
    assert resp.status_code == 400

def test_json_with_large_object(simple_app):
    app_client = simple_app.test_client()
    large_object = {str(i): i for i in range(1000)}
    resp = app_client.post(
        "/v1.0/test-json-with-large-object",
        json=large_object,
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response["stack"] == large_object

def test_json_with_nested_object(simple_app):
    app_client = simple_app.test_client()
    nested_object = {"key": {"subkey": "value"}}
    resp = app_client.post(
        "/v1.0/test-json-with-nested-object",
        json=nested_object,
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response["stack"] == nested_object