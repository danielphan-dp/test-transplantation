import json
import pytest

def test_json_valid(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    valid_json_request = app_client.post("/v1.0/json", json={"key": "value"})
    assert valid_json_request.status_code == 200
    assert valid_json_request.headers.get("content-type") == "application/json"
    assert valid_json_request.json() == {"key": "value"}

def test_json_invalid(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    invalid_json_request = app_client.post("/v1.0/json", json="invalid json")
    assert invalid_json_request.status_code == 400
    assert invalid_json_request.headers.get("content-type") == "application/json"
    assert "error" in invalid_json_request.json()

def test_json_empty(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    empty_json_request = app_client.post("/v1.0/json", json={})
    assert empty_json_request.status_code == 200
    assert empty_json_request.headers.get("content-type") == "application/json"
    assert empty_json_request.json() == {}