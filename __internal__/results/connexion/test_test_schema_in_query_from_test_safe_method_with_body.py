import json
import pytest

def test_json_method_with_valid_data(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    valid_data = json.dumps({"key": "value"})

    response = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data=valid_data,
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["key"] == "value"

def test_json_method_with_empty_data(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    response = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data="",
    )
    assert response.status_code == 400

def test_json_method_with_invalid_json(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    invalid_data = "{key: value}"  # Invalid JSON

    response = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data=invalid_data,
    )
    assert response.status_code == 400

def test_json_method_with_non_json_content(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "text/plain"}

    response = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data="This is not JSON",
    )
    assert response.status_code == 400