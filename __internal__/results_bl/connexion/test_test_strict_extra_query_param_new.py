import json
import pytest
from io import BytesIO
from typing import List

def test_json_method_with_valid_json(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    valid_json = '{"key": "value"}'
    resp = app_client.post("/v1.0/test_json", data=valid_json, headers=headers)
    assert resp.status_code == 200
    response = resp.json()
    assert response["key"] == "value"

def test_json_method_with_invalid_json(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    invalid_json = '{"key": "value"'
    resp = app_client.post("/v1.0/test_json", data=invalid_json, headers=headers)
    assert resp.status_code == 400
    response = resp.json()
    assert response["detail"] == "Invalid JSON format"

def test_json_method_with_empty_body(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post("/v1.0/test_json", data='', headers=headers)
    assert resp.status_code == 400
    response = resp.json()
    assert response["detail"] == "Empty request body"

def test_json_method_with_non_json_content(strict_app):
    app_client = strict_app.test_client()
    headers = {"Content-type": "text/plain"}
    resp = app_client.post("/v1.0/test_json", data='Just a plain text', headers=headers)
    assert resp.status_code == 415
    response = resp.json()
    assert response["detail"] == "Unsupported Media Type"