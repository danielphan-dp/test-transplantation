import pytest

def test_post_method_with_valid_kwargs(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_kwargs(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_additional_kwargs(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", json={"extra": "data"})
    assert response.status_code == 201
    assert response.json() == {"extra": "data", "name": "post"}

def test_post_method_with_invalid_data(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", data="invalid data")
    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid data

def test_post_method_cors_headers(cors_openapi_app):
    app_client = cors_openapi_app.test_client()
    origin = "http://localhost"
    response = app_client.post("/v1.0/goodday/dan", json={}, headers={"Origin": origin})
    assert response.status_code == 201
    assert "Access-Control-Allow-Origin" in response.headers
    assert origin == response.headers["Access-Control-Allow-Origin"]