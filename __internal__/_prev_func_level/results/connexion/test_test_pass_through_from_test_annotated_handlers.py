import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_json_parsing_valid(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/json", json={"key": "value"})
    assert response.status_code == 200
    assert response.json == {"key": "value"}

def test_json_parsing_invalid(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/json", data="invalid json")
    assert response.status_code == 400
    detail = response.json["detail"]
    assert detail == "Invalid JSON input."

def test_json_parsing_empty(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/json", json={})
    assert response.status_code == 200
    assert response.json == {}

def test_json_parsing_malformed(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/json", data='{"key": "value",}')
    assert response.status_code == 400
    detail = response.json["detail"]
    assert detail == "Malformed JSON input."