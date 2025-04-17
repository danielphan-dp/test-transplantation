import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_json_method(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    # Test with valid JSON string
    response = app_client.post(
        "/v1.0/json_test",
        data=json.dumps({"key": "value"}),
        content_type='application/json'
    )
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    json_response = response.json()
    assert json_response["key"] == "value"

    # Test with invalid JSON string
    response = app_client.post(
        "/v1.0/json_test",
        data="invalid json",
        content_type='application/json'
    )
    assert response.status_code == 400

    # Test with empty JSON
    response = app_client.post(
        "/v1.0/json_test",
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response == {}

    # Test with nested JSON
    response = app_client.post(
        "/v1.0/json_test",
        data=json.dumps({"nested": {"key": "value"}}),
        content_type='application/json'
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["nested"]["key"] == "value"