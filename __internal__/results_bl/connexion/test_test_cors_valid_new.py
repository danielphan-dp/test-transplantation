import json
import pytest

def test_post_method_with_valid_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", data=json.dumps({"key": "value"}), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'name': 'post', 'key': 'value'}

def test_post_method_with_empty_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", data=json.dumps({}), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'name': 'post'}

def test_post_method_with_invalid_json(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", data="invalid json", content_type='application/json')
    assert response.status_code == 400

def test_post_method_with_missing_parameters(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", data=json.dumps({"missing_key": "value"}), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'name': 'post', 'missing_key': 'value'}