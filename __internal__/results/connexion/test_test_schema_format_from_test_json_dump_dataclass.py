import json
import pytest

def test_json_invalid_type(schema_app):
    app_client = schema_app.test_client()
    
    invalid_json = app_client.post("/v1.0/test_json_invalid_type", json=123)
    assert invalid_json.status_code == 400
    assert invalid_json.headers.get("content-type") == "application/problem+json"
    invalid_json_response = invalid_json.json()
    assert invalid_json_response["title"] == "Bad Request"
    assert "'123' is not of type 'object'" in invalid_json_response["detail"]

def test_json_empty_string(schema_app):
    app_client = schema_app.test_client()
    
    empty_string = app_client.post("/v1.0/test_json_empty_string", json="")
    assert empty_string.status_code == 400
    assert empty_string.headers.get("content-type") == "application/problem+json"
    empty_string_response = empty_string.json()
    assert empty_string_response["title"] == "Bad Request"
    assert "' is not of type 'object'" in empty_string_response["detail"]

def test_json_none_value(schema_app):
    app_client = schema_app.test_client()
    
    none_value = app_client.post("/v1.0/test_json_none_value", json=None)
    assert none_value.status_code == 400
    assert none_value.headers.get("content-type") == "application/problem+json"
    none_value_response = none_value.json()
    assert none_value_response["title"] == "Bad Request"
    assert "'None' is not of type 'object'" in none_value_response["detail"]