import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    payload = json.dumps({"key": "value"})
    resp = app_client.post("/v1.0/test-json-method", data=payload, content_type='application/json')
    assert resp.status_code == 200, resp.text
    response = resp.json()
    assert response == {"key": "value"}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_payload = "{key: value}"  # Invalid JSON
    resp = app_client.post("/v1.0/test-json-method", data=invalid_payload, content_type='application/json')
    assert resp.status_code == 400, resp.text
    response = resp.json()
    assert "error" in response

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json-method", data='', content_type='application/json')
    assert resp.status_code == 400, resp.text
    response = resp.json()
    assert "error" in response

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json-method", data="Just a string", content_type='text/plain')
    assert resp.status_code == 415, resp.text
    response = resp.json()
    assert "error" in response

def test_json_method_with_large_payload(simple_app):
    app_client = simple_app.test_client()
    large_payload = json.dumps({"key": "value" * 10000})  # Large JSON
    resp = app_client.post("/v1.0/test-json-method", data=large_payload, content_type='application/json')
    assert resp.status_code == 200, resp.text
    response = resp.json()
    assert response == {"key": "value" * 10000}