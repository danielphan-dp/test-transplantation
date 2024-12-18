import json
import pytest
from connexion import App

def test_json_method(secure_endpoint_app):
    app_client = secure_endpoint_app.test_client()

    # Test with valid JSON string
    valid_json_response = app_client.get("/v1.0/valid-json")
    assert valid_json_response.status_code == 200
    assert valid_json_response.json() == {"message": "Valid JSON"}

    # Test with invalid JSON string
    invalid_json_response = app_client.get("/v1.0/invalid-json")
    assert invalid_json_response.status_code == 400
    assert invalid_json_response.headers.get("content-type") == "application/problem+json"
    invalid_json_response_data = invalid_json_response.json()
    assert invalid_json_response_data["detail"] == "Invalid JSON format"

    # Test with empty JSON string
    empty_json_response = app_client.get("/v1.0/empty-json")
    assert empty_json_response.status_code == 400
    assert empty_json_response.headers.get("content-type") == "application/problem+json"
    empty_json_response_data = empty_json_response.json()
    assert empty_json_response_data["detail"] == "Empty JSON string"

    # Test with JSON containing unexpected data types
    unexpected_type_response = app_client.get("/v1.0/unexpected-type-json")
    assert unexpected_type_response.status_code == 400
    assert unexpected_type_response.headers.get("content-type") == "application/problem+json"
    unexpected_type_response_data = unexpected_type_response.json()
    assert unexpected_type_response_data["detail"].startswith("Unexpected data type")

    # Test with valid JSON but missing required fields
    missing_field_response = app_client.get("/v1.0/missing-field-json")
    assert missing_field_response.status_code == 400
    assert missing_field_response.headers.get("content-type") == "application/problem+json"
    missing_field_response_data = missing_field_response.json()
    assert missing_field_response_data["detail"] == "Missing required fields"