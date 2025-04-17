import json
import pytest

def test_json_method_with_valid_json(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-json", data=json.dumps({"key": "value"}), content_type='application/json')
    assert resp.status_code == 200
    assert resp.json == {"key": "value"}

def test_json_method_with_invalid_json(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="invalid json", content_type='application/json')
    assert resp.status_code == 400
    assert resp.json["detail"] == "Invalid JSON"

def test_json_method_with_empty_json(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-json", data=json.dumps({}), content_type='application/json')
    assert resp.status_code == 200
    assert resp.json == {}

def test_json_method_with_non_json_data(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="text data", content_type='text/plain')
    assert resp.status_code == 400
    assert resp.json["detail"] == "Invalid content type"