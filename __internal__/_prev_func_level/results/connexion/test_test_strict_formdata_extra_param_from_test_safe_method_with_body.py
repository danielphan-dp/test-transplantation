import json
import pytest

def test_json_method_with_valid_json(strict_app):
    app_client = strict_app.test_client()
    valid_json = json.dumps({"key": "value"})
    resp = app_client.post("/v1.0/test-json", data=valid_json, content_type='application/json')
    assert resp.status_code == 200
    assert resp.json == {"key": "value"}

def test_json_method_with_invalid_json(strict_app):
    app_client = strict_app.test_client()
    invalid_json = "{key: value}"  # Invalid JSON format
    resp = app_client.post("/v1.0/test-json", data=invalid_json, content_type='application/json')
    assert resp.status_code == 400
    assert resp.json["detail"] == "Invalid JSON format"

def test_json_method_with_empty_body(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="", content_type='application/json')
    assert resp.status_code == 400
    assert resp.json["detail"] == "Empty request body"

def test_json_method_with_non_json_content(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="Just a string", content_type='text/plain')
    assert resp.status_code == 415
    assert resp.json["detail"] == "Unsupported Media Type"