import json
import pytest

def test_json_method(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    # Test with valid JSON
    valid_request = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        json={"key": "value"},
    )
    assert valid_request.status_code == 200
    valid_response = valid_request.json()
    assert valid_response["key"] == "value"

    # Test with invalid JSON
    invalid_request = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        data="not a json",
    )
    assert invalid_request.status_code == 400

    # Test with empty JSON
    empty_request = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        json={},
    )
    assert empty_request.status_code == 200
    empty_response = empty_request.json()
    assert empty_response == {}

    # Test with nested JSON
    nested_request = app_client.post(
        "/v1.0/test_json_method",
        headers=headers,
        json={"nested": {"key": "value"}},
    )
    assert nested_request.status_code == 200
    nested_response = nested_request.json()
    assert nested_response["nested"]["key"] == "value"