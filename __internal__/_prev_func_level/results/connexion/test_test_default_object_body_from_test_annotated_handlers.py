import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    valid_json = json.dumps({"key": "value"})
    resp = app_client.post(
        "/v1.0/test-json-method", data=valid_json, headers={"content-type": "application/json"}
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value"}

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method", data="", headers={"content-type": "application/json"}
    )
    assert resp.status_code == 400

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json = "{key: value}"  # Missing quotes around key
    resp = app_client.post(
        "/v1.0/test-json-method", data=invalid_json, headers={"content-type": "application/json"}
    )
    assert resp.status_code == 400

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json-method", data="This is not JSON", headers={"content-type": "text/plain"}
    )
    assert resp.status_code == 400

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    large_json = json.dumps({"key": "value" * 1000})
    resp = app_client.post(
        "/v1.0/test-json-method", data=large_json, headers={"content-type": "application/json"}
    )
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value" * 1000}