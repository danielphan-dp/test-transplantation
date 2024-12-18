import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_json_empty_string(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/greeting/")
    assert response.status_code == 400
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json()
    assert response_data["error"] == "Invalid input"

def test_json_invalid_format(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/greeting/jsantos", data="invalid_json")
    assert response.status_code == 400
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json()
    assert response_data["error"] == "Invalid JSON format"

def test_json_response_structure(simple_app):
    app_client = simple_app.test_client()
    post_greeting = app_client.post("/v1.0/greeting/jsantos")
    assert post_greeting.status_code == 200
    assert post_greeting.headers.get("content-type") == "application/json"
    greeting_response = post_greeting.json()
    assert "greeting" in greeting_response
    assert isinstance(greeting_response["greeting"], str)

def test_json_response_content_type(simple_app):
    app_client = simple_app.test_client()
    post_greeting = app_client.post("/v1.0/greeting/jsantos")
    assert post_greeting.headers.get("content-type") == "application/json"

def test_json_with_special_characters(simple_app):
    app_client = simple_app.test_client()
    post_greeting = app_client.post("/v1.0/greeting/jsantos@!")
    assert post_greeting.status_code == 200
    greeting_response = post_greeting.json()
    assert greeting_response["greeting"] == "Hello jsantos@!"