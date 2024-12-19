import json
import pytest

def test_should_raise_400_for_invalid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-invalid-json", json="invalid_json")
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid JSON format"

def test_should_raise_400_for_non_json_content(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-non-json-content", data="This is not JSON")
    assert response.status_code == 400
    assert response.json()["detail"] == "Request body must be JSON"

def test_should_return_200_for_valid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-valid-json", json={"key": "value"})
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_should_raise_400_for_empty_json_object(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-empty-json-object", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Request body must not be empty"