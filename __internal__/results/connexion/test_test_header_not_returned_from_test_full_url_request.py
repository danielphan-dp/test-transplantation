import pytest

def test_post_method_with_valid_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_unexpected_key(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday", json={"unexpected_key": "value"})
    assert response.status_code == 201
    assert response.json() == {"unexpected_key": "value", "name": "post"}

def test_post_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday", data="invalid_json")
    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

def test_post_method_with_missing_endpoint(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.post("/v1.0/nonexistent", json={"key": "value"})
    assert response.status_code == 404  # Assuming the endpoint does not exist