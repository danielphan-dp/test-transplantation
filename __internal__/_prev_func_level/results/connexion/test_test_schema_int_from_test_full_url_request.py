import pytest

def test_post_method_with_valid_data(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post("/v1.0/post", json={"key": "value"})
    assert response.status_code == 201
    assert response.headers.get("content-type") == "application/json"
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.headers.get("content-type") == "application/json"
    assert response.json() == {"name": "post"}

def test_post_method_with_invalid_data(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post("/v1.0/post", json="invalid_data")
    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON
    assert response.headers.get("content-type") == "application/json"