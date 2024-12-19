import json
import pytest

def test_post_method_with_valid_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday", data=json.dumps({"key": "value"}), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'key': 'value', 'name': 'post'}

def test_post_method_with_empty_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday", data=json.dumps({}), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'name': 'post'}

def test_post_method_with_invalid_json(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday", data="invalid_json", content_type='application/json')
    assert response.status_code == 400

def test_post_method_with_missing_endpoint(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/nonexistent", data=json.dumps({"key": "value"}), content_type='application/json')
    assert response.status_code == 404

def test_post_method_with_no_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday", data=None)
    assert response.status_code == 400