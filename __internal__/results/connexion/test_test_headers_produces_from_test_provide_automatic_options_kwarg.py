import pytest

def test_post_method_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodevening/dan", json={"key": "value"})
    assert response.status_code == 201
    assert response.json == {"key": "value", "name": "post"}

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodevening/dan", json={})
    assert response.status_code == 201
    assert response.json == {"name": "post"}

def test_post_method_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodevening/dan", json={"extra": "data"})
    assert response.status_code == 201
    assert response.json == {"extra": "data", "name": "post"}

def test_post_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodevening/dan", json="invalid_data")
    assert response.status_code == 400  # Assuming the API returns 400 for invalid JSON

def test_post_method_with_missing_endpoint(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/nonexistent", json={})
    assert response.status_code == 404  # Assuming the API returns 404 for nonexistent endpoints