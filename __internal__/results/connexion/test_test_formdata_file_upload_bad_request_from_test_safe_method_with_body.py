import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    valid_data = json.dumps({"key": "value"})
    response = app_client.post(
        "/v1.0/test-json",
        data=valid_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_data = "{key: value}"  # Invalid JSON format
    response = app_client.post(
        "/v1.0/test-json",
        data=invalid_data,
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid JSON format"

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post(
        "/v1.0/test-json",
        data="",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Empty request body"