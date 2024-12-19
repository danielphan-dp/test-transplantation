import json
import pytest
from io import BytesIO

def test_json_method_with_empty_text(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="")
    assert resp.status_code == 200
    assert resp.json() == {}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data="invalid json")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid JSON format"

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    valid_json = json.dumps({"key": "value"})
    resp = app_client.post("/v1.0/test-json", data=valid_json, content_type='application/json')
    assert resp.status_code == 200
    assert resp.json() == {"key": "value"}

def test_json_method_with_partial_json(simple_app):
    app_client = simple_app.test_client()
    partial_json = json.dumps({"key": None})
    resp = app_client.post("/v1.0/test-json", data=partial_json, content_type='application/json')
    assert resp.status_code == 200
    assert resp.json() == {"key": None}