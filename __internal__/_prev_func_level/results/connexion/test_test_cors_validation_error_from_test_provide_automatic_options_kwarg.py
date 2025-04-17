import pytest

def test_post_method_with_valid_kwargs(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/post-endpoint", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_kwargs(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/post-endpoint", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_additional_properties(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/post-endpoint", json={"extra": "data"})
    assert response.status_code == 201
    assert response.json() == {"extra": "data", "name": "post"}

def test_post_method_with_invalid_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/post-endpoint", data="invalid data")
    assert response.status_code == 400

def test_post_method_with_missing_endpoint(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/nonexistent-endpoint", json={"key": "value"})
    assert response.status_code == 404