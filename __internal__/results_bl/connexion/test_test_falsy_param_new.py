import json
import pytest
from io import BytesIO
from typing import List

def test_json_method_with_valid_json(simple_app):
    app_client = simple_app.test_client()
    valid_json = '{"key": "value"}'
    resp = app_client.post("/v1.0/test-json", data=valid_json, content_type='application/json')
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value"}

def test_json_method_with_empty_string(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data='', content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json = '{"key": "value"'
    resp = app_client.post("/v1.0/test-json", data=invalid_json, content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_non_json_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-json", data='plain text', content_type='text/plain')
    assert resp.status_code == 415

def test_json_method_with_large_json(simple_app):
    app_client = simple_app.test_client()
    large_json = json.dumps({"key": "value" * 10000})
    resp = app_client.post("/v1.0/test-json", data=large_json, content_type='application/json')
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value" * 10000}