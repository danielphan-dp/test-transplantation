import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    valid_json = json.dumps({"key": "value"})
    resp = app_client.post(
        "/v1.0/test-json-method", data=valid_json, headers={"content-type": "application/json"}
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value"}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json = "{key: value}"  # Invalid JSON format
    resp = app_client.post(
        "/v1.0/test-json-method", data=invalid_json, headers={"content-type": "application/json"}
    )
    assert resp.status_code == 400  # Expecting a bad request due to invalid JSON

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method", data="", headers={"content-type": "application/json"}
    )
    assert resp.status_code == 400  # Expecting a bad request due to empty body

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method", data="Not a JSON", headers={"content-type": "text/plain"}
    )
    assert resp.status_code == 415  # Expecting unsupported media type due to non-JSON content