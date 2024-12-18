import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value"}
    resp = app_client.request(
        "POST",
        "/v1.0/json-method",
        json=body,
    )
    assert resp.status_code == 200
    assert resp.json() == body

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    body = {}
    resp = app_client.request(
        "POST",
        "/v1.0/json-method",
        json=body,
    )
    assert resp.status_code == 200
    assert resp.json() == body

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    body = "{invalid_json}"
    resp = app_client.request(
        "POST",
        "/v1.0/json-method",
        data=body,
        content_type='application/json',
    )
    assert resp.status_code == 400

def test_json_method_with_non_json_content(simple_app):
    app_client = simple_app.test_client()
    body = "Just a string"
    resp = app_client.request(
        "POST",
        "/v1.0/json-method",
        data=body,
        content_type='text/plain',
    )
    assert resp.status_code == 415

def test_json_method_with_large_data(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value" * 1000}
    resp = app_client.request(
        "POST",
        "/v1.0/json-method",
        json=body,
    )
    assert resp.status_code == 200
    assert resp.json() == body