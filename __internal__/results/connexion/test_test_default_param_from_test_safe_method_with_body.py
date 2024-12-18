import json
import pytest

def test_json_method_with_valid_data(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.get("/v1.0/test-json-valid")
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value"}

def test_json_method_with_empty_data(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.get("/v1.0/test-json-empty")
    assert resp.status_code == 200
    response = resp.json()
    assert response == {}

def test_json_method_with_invalid_json(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.get("/v1.0/test-json-invalid")
    assert resp.status_code == 400
    response = resp.json()
    assert "error" in response

def test_json_method_with_non_json_response(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.get("/v1.0/test-json-non-json")
    assert resp.status_code == 200
    response = resp.data.decode('utf-8')
    assert response == "This is not JSON"