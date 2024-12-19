import json
import pytest

def test_json_method_empty_string(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_json_empty"
    resp = app_client.post(url, headers=headers, data=json.dumps({"text": ""}))
    response = resp.json()
    assert response == {}
    assert resp.status_code == 200

def test_json_method_invalid_json(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_json_invalid"
    resp = app_client.post(url, headers=headers, data="invalid json")
    assert resp.status_code == 400

def test_json_method_non_json_content(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "text/plain"}
    url = "/v1.0/test_json_non_json"
    resp = app_client.post(url, headers=headers, data="Just a plain text")
    assert resp.status_code == 415

def test_json_method_valid_json(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_json_valid"
    resp = app_client.post(url, headers=headers, data=json.dumps({"text": "valid json"}))
    response = resp.json()
    assert response == {"text": "valid json"}
    assert resp.status_code == 200

def test_json_method_missing_key(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_json_missing_key"
    resp = app_client.post(url, headers=headers, data=json.dumps({}))
    assert resp.status_code == 400