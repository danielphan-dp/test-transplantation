import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value"}
    resp = app_client.post(
        "/v1.0/test-json",
        json=body,
    )
    assert resp.status_code == 200
    response_data = resp.json()
    assert response_data == body

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    body = "{invalid_json}"
    resp = app_client.post(
        "/v1.0/test-json",
        data=body,
        content_type='application/json',
    )
    assert resp.status_code == 400
    response = resp.json()
    assert "Invalid JSON" in response["detail"]

def test_json_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-json",
        json={},
    )
    assert resp.status_code == 200
    response_data = resp.json()
    assert response_data == {}

def test_json_method_with_additional_properties(simple_app):
    app_client = simple_app.test_client()
    body = {"key": "value", "extra_key": "extra_value"}
    resp = app_client.post(
        "/v1.0/test-json",
        json=body,
    )
    assert resp.status_code == 400
    response = resp.json()
    assert "Additional properties are not allowed" in response["detail"]