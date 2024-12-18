import json
import pytest

def test_json_method_with_empty_string(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-empty-string",
        data='',
    )
    assert resp.status_code == 400

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-invalid",
        data='{"invalid_json":}',
    )
    assert resp.status_code == 400

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-valid",
        json={"key": "value"},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response["key"] == "value"

def test_json_method_with_nested_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-nested",
        json={"outer": {"inner": "value"}},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response["outer"]["inner"] == "value"