import pytest

def test_post_method_with_valid_data(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/post", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_additional_data(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/post", json={"extra": "data"})
    assert response.status_code == 201
    assert response.json() == {"extra": "data", "name": "post"}

def test_post_method_with_invalid_json(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/post", data="invalid json")
    assert response.status_code == 400

def test_post_method_with_missing_key(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/post", json={"name": "post"})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}