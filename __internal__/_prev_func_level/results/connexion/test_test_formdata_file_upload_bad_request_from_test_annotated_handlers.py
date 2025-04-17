import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    valid_json = json.dumps({"key": "value"})
    resp = app_client.post(
        "/v1.0/test-json",
        data=valid_json,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 200
    assert resp.json == {"key": "value"}

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json = "{key: value}"  # Missing quotes around key
    resp = app_client.post(
        "/v1.0/test-json",
        data=invalid_json,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400
    assert resp.json["detail"] == "Invalid JSON format"

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json",
        data="",
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400
    assert resp.json["detail"] == "Empty request body"

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json",
        data="This is not JSON",
        headers={"Content-Type": "text/plain"},
    )
    assert resp.status_code == 400
    assert resp.json["detail"] == "Invalid content type"