import json
import pytest

def test_json_method_with_valid_json(strict_app):
    app_client = strict_app.test_client()
    valid_json = '{"app_name": "connexion"}'
    resp = app_client.post("/v1.0/test-json", data=valid_json, content_type='application/json')
    assert resp.status_code == 200
    response = resp.json()
    assert response["app_name"] == "connexion"

def test_json_method_with_invalid_json(strict_app):
    app_client = strict_app.test_client()
    invalid_json = '{"app_name": "connexion"'
    resp = app_client.post("/v1.0/test-json", data=invalid_json, content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_empty_json(strict_app):
    app_client = strict_app.test_client()
    empty_json = '{}'
    resp = app_client.post("/v1.0/test-json", data=empty_json, content_type='application/json')
    assert resp.status_code == 200
    response = resp.json()
    assert response == {}

def test_json_method_with_non_json_data(strict_app):
    app_client = strict_app.test_client()
    non_json_data = 'Just a string'
    resp = app_client.post("/v1.0/test-json", data=non_json_data, content_type='text/plain')
    assert resp.status_code == 400