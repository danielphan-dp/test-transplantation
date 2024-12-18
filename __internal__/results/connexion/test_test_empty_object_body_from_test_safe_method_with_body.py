import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        json={"key": "value"},
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response["key"] == "value"

def test_json_method_with_empty_string(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data='',
        content_type='application/json'
    )
    assert resp.status_code == 400

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data='{"key": "value",}',
        content_type='application/json'
    )
    assert resp.status_code == 400

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method",
        data='This is not JSON',
        content_type='text/plain'
    )
    assert resp.status_code == 400

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    large_payload = {"key": "value" * 1000}
    resp = app_client.post(
        "/v1.0/test-json-method",
        json=large_payload,
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response["key"] == large_payload["key"]