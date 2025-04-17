import json
import pytest
from connexion import App
from connexion.lifecycle import ConnexionRequest, ConnexionResponse

@pytest.fixture
def app_class():
    return App

@pytest.fixture
def simple_api_spec_dir():
    return "path/to/spec"

def test_json_method(app_class, simple_api_spec_dir):
    app = app_class(__name__, specification_dir=simple_api_spec_dir)
    app_client = app.test_client()

    # Test with valid JSON
    valid_json_response = app_client.post("/json_endpoint", json={"key": "value"})
    assert valid_json_response.status_code == 200
    assert valid_json_response.json == {"key": "value"}

    # Test with invalid JSON
    invalid_json_response = app_client.post("/json_endpoint", data="not a json")
    assert invalid_json_response.status_code == 400
    assert invalid_json_response.json["error"] == "Invalid JSON"

    # Test with empty JSON
    empty_json_response = app_client.post("/json_endpoint", json={})
    assert empty_json_response.status_code == 200
    assert empty_json_response.json == {}

    # Test with malformed JSON
    malformed_json_response = app_client.post("/json_endpoint", data="{key: value}")
    assert malformed_json_response.status_code == 400
    assert malformed_json_response.json["error"] == "Malformed JSON"