import json
import pytest
from connexion import App

def test_json_method_with_valid_json(secure_endpoint_strict_app):
    app_client = secure_endpoint_strict_app.test_client()
    valid_json = '{"key": "value"}'
    response = app_client.post("/v1.0/test_json", data=valid_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_json_method_with_invalid_json(secure_endpoint_strict_app):
    app_client = secure_endpoint_strict_app.test_client()
    invalid_json = '{"key": "value"'
    response = app_client.post("/v1.0/test_json", data=invalid_json, content_type='application/json')
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid JSON"

def test_json_method_with_empty_string(secure_endpoint_strict_app):
    app_client = secure_endpoint_strict_app.test_client()
    response = app_client.post("/v1.0/test_json", data='', content_type='application/json')
    assert response.status_code == 400
    assert response.json()["detail"] == "Empty JSON body"

def test_json_method_with_non_json_content(secure_endpoint_strict_app):
    app_client = secure_endpoint_strict_app.test_client()
    response = app_client.post("/v1.0/test_json", data='Not a JSON', content_type='text/plain')
    assert response.status_code == 415
    assert response.json()["detail"] == "Unsupported Media Type"