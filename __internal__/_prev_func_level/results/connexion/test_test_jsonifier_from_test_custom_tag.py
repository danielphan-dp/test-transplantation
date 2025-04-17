import json
import pytest
from connexion.FlaskApp import FlaskApp
from connexion.frameworks.flask.FlaskJSONProvider import FlaskJSONProvider
from conftest import build_app_from_fixture

def test_json_method(simple_app):
    app_client = simple_app.test_client()

    # Test valid JSON response
    post_greeting = app_client.post("/v1.0/greeting/jsantos")
    assert post_greeting.status_code == 200
    assert post_greeting.headers.get("content-type") == "application/json"
    greeting_response = post_greeting.json()
    assert greeting_response["greeting"] == "Hello jsantos"

    # Test JSON deserialization with invalid data
    invalid_json_response = app_client.post("/v1.0/greeting/invalid")
    assert invalid_json_response.status_code == 400
    assert invalid_json_response.headers.get("content-type") == "application/json"
    error_response = invalid_json_response.json()
    assert "error" in error_response

    # Test empty JSON response
    empty_response = app_client.get("/v1.0/list/empty")
    assert empty_response.status_code == 200
    assert empty_response.headers.get("content-type") == "application/json"
    empty_greeting_response = empty_response.json()
    assert len(empty_greeting_response) == 0

    # Test JSON response with unexpected structure
    unexpected_response = app_client.get("/v1.0/greetings/unexpected")
    assert unexpected_response.status_code == 200
    assert unexpected_response.headers.get("content-type") == "application/x.connexion+json"
    unexpected_greetings_response = unexpected_response.json()
    assert "unexpected_key" not in unexpected_greetings_response

    # Test JSON deserialization of non-JSON content
    non_json_response = app_client.post("/v1.0/greeting/non_json")
    assert non_json_response.status_code == 400
    assert non_json_response.headers.get("content-type") == "application/json"
    non_json_error_response = non_json_response.json()
    assert "error" in non_json_error_response