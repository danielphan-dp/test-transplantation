import pytest

def test_post_method_with_valid_kwargs(middleware_app):
    app_client = middleware_app.test_client()
    response = app_client.post("/v1.0/post", json={"key": "value"})
    
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_kwargs(middleware_app):
    app_client = middleware_app.test_client()
    response = app_client.post("/v1.0/post", json={})
    
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_additional_kwargs(middleware_app):
    app_client = middleware_app.test_client()
    response = app_client.post("/v1.0/post", json={"extra": "data"})
    
    assert response.status_code == 201
    assert response.json() == {"extra": "data", "name": "post"}

def test_post_method_with_invalid_data(middleware_app):
    app_client = middleware_app.test_client()
    response = app_client.post("/v1.0/post", json="invalid_data")
    
    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

def test_post_method_with_missing_endpoint(middleware_app):
    app_client = middleware_app.test_client()
    response = app_client.post("/v1.0/nonexistent", json={"key": "value"})
    
    assert response.status_code == 404  # Assuming the endpoint does not exist