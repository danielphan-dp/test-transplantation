import json
import pytest

def test_json_method_with_valid_json(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_json"
    data = json.dumps({"key": "value"})
    resp = app_client.post(url, headers=headers, data=data)
    response = resp.json()
    assert response == {"key": "value"}
    assert resp.status_code == 200

def test_json_method_with_invalid_json(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_json"
    data = "{invalid_json}"
    resp = app_client.post(url, headers=headers, data=data)
    assert resp.status_code == 400

def test_json_method_with_empty_body(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_json"
    resp = app_client.post(url, headers=headers, data="")
    assert resp.status_code == 400

def test_json_method_with_non_json_content(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "text/plain"}
    url = "/v1.0/test_json"
    data = "Just a plain text"
    resp = app_client.post(url, headers=headers, data=data)
    assert resp.status_code == 415