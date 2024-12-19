import json
import pytest

def test_post_method_with_valid_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post(
        "/v1.0/post-endpoint",
        data=json.dumps({"key": "value"}),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.json == {'key': 'value', 'name': 'post'}

def test_post_method_with_empty_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post(
        "/v1.0/post-endpoint",
        data=json.dumps({}),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.json == {'name': 'post'}

def test_post_method_with_invalid_json(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post(
        "/v1.0/post-endpoint",
        data="invalid json",
        content_type='application/json'
    )
    assert response.status_code == 400

def test_post_method_with_missing_key(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post(
        "/v1.0/post-endpoint",
        data=json.dumps({"name": "post"}),
        content_type='application/json'
    )
    assert response.status_code == 201
    assert response.json == {'name': 'post'}