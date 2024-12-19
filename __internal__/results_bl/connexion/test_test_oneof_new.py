import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_openapi_app():
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/oneof_greeting", query_string={"name": 3})
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json
    assert response_data["name"] == 3

    response = app_client.get("/v1.0/oneof_greeting", query_string={"name": True})
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json
    assert response_data["name"] is True

    response = app_client.get("/v1.0/oneof_greeting", query_string={"name": "test"})
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json
    assert response_data["name"] == "test"

def test_get_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/oneof_greeting")
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json
    assert response_data == [{'name': 'get'}]