import json
import pytest
from connexion.lifecycle import ConnexionRequest, ConnexionResponse

def test_add_error_handler_invalid_method(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")

    def method_not_allowed(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
        return ConnexionResponse(
            status_code=405, body=json.dumps({"error": "MethodNotAllowed"})
        )

    app.add_error_handler(405, method_not_allowed)

    app_client = app.test_client()

    response = app_client.post("/does_not_exist")
    assert response.status_code == 405
    assert response.json()["error"] == "MethodNotAllowed"

def test_add_error_handler_internal_server_error(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")

    def internal_server_error(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
        return ConnexionResponse(
            status_code=500, body=json.dumps({"error": "InternalServerError"})
        )

    app.add_error_handler(500, internal_server_error)

    app_client = app.test_client()

    response = app_client.get("/trigger_internal_error")
    assert response.status_code == 500
    assert response.json()["error"] == "InternalServerError"

def test_add_error_handler_custom_error(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app.add_api("openapi.yaml")

    def custom_error_handler(request: ConnexionRequest, exc: Exception) -> ConnexionResponse:
        return ConnexionResponse(
            status_code=418, body=json.dumps({"error": "I'm a teapot"})
        )

    app.add_error_handler(418, custom_error_handler)

    app_client = app.test_client()

    response = app_client.get("/teapot")
    assert response.status_code == 418
    assert response.json()["error"] == "I'm a teapot"