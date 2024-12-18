import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    valid_data = json.dumps({"key": "value"})
    resp = app_client.post("/v1.0/test-json", data=valid_data, content_type='application/json')
    assert resp.status_code == 200
    response = resp.json()
    assert response["key"] == "value"

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_data = "{key: value}"  # Invalid JSON format
    resp = app_client.post("/v1.0/test-json", data=invalid_data, content_type='application/json')
    assert resp.status_code == 400
    response = resp.json()
    assert response["detail"] == "Invalid JSON format"

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data='', content_type='application/json')
    assert resp.status_code == 400
    response = resp.json()
    assert response["detail"] == "Empty request body"

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="Just a string", content_type='text/plain')
    assert resp.status_code == 415
    response = resp.json()
    assert response["detail"] == "Unsupported Media Type"