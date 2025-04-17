import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data=json.dumps({"key": "value"}), content_type='application/json')
    assert resp.status_code == 200, resp.text
    response = resp.json()
    assert response == {"key": "value"}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="invalid json", content_type='application/json')
    assert resp.status_code == 400, resp.text
    response = resp.json()
    assert "error" in response

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="", content_type='application/json')
    assert resp.status_code == 400, resp.text
    response = resp.json()
    assert "error" in response

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    large_data = json.dumps({"key": "value" * 10000})
    resp = app_client.post("/v1.0/test-json", data=large_data, content_type='application/json')
    assert resp.status_code == 200, resp.text
    response = resp.json()
    assert response == {"key": "value" * 10000}