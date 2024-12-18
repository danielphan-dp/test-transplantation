import json
import pytest

def test_json_empty_string(schema_app):
    app_client = schema_app.test_client()
    empty_request = app_client.post("/v1.0/schema_array", json="")
    assert empty_request.status_code == 400
    assert empty_request.headers.get("content-type") == "application/json"
    empty_response = empty_request.json()
    assert "error" in empty_response

def test_json_invalid_data(schema_app):
    app_client = schema_app.test_client()
    invalid_request = app_client.post("/v1.0/schema_array", json={"key": "value"})
    assert invalid_request.status_code == 400
    assert invalid_request.headers.get("content-type") == "application/json"
    invalid_response = invalid_request.json()
    assert "error" in invalid_response

def test_json_large_array(schema_app):
    app_client = schema_app.test_client()
    large_array = list(range(1000))
    large_request = app_client.post("/v1.0/schema_array", json=large_array)
    assert large_request.status_code == 200
    assert large_request.headers.get("content-type") == "application/json"
    large_response = large_request.json()
    assert large_response == large_array

def test_json_non_serializable(schema_app):
    app_client = schema_app.test_client()
    non_serializable_request = app_client.post("/v1.0/schema_array", json=set([1, 2, 3]))
    assert non_serializable_request.status_code == 400
    assert non_serializable_request.headers.get("content-type") == "application/json"
    non_serializable_response = non_serializable_request.json()
    assert "error" in non_serializable_response

def test_json_valid_array_with_special_characters(schema_app):
    app_client = schema_app.test_client()
    special_characters_request = app_client.post("/v1.0/schema_array", json=["list", "hello", "!@#$%^&*()"])
    assert special_characters_request.status_code == 200
    assert special_characters_request.headers.get("content-type") == "application/json"
    special_characters_response = special_characters_request.json()
    assert special_characters_response == ["list", "hello", "!@#$%^&*()"]