import json
import pytest

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value"}
    resp = app_client.request(
        "GET",
        "/v1.0/body-in-get-request",
        json=body,
    )
    assert resp.status_code == 200
    assert resp.json() == body

def test_json_method_with_empty_json(simple_app):
    app_client = simple_app.test_client()
    body = {}
    resp = app_client.request(
        "GET",
        "/v1.0/body-in-get-request",
        json=body,
    )
    assert resp.status_code == 200
    assert resp.json() == body

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    body = "invalid json"
    resp = app_client.request(
        "GET",
        "/v1.0/body-in-get-request",
        data=body,
    )
    assert resp.status_code == 400

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value" * 1000}
    resp = app_client.request(
        "GET",
        "/v1.0/body-in-get-request",
        json=body,
    )
    assert resp.status_code == 200
    assert resp.json() == body

def test_json_method_with_nested_json(simple_app):
    app_client = simple_app.test_client()
    body = {"outer": {"inner": "value"}}
    resp = app_client.request(
        "GET",
        "/v1.0/body-in-get-request",
        json=body,
    )
    assert resp.status_code == 200
    assert resp.json() == body

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    body = "<html></html>"
    resp = app_client.request(
        "GET",
        "/v1.0/body-in-get-request",
        data=body,
    )
    assert resp.status_code == 400