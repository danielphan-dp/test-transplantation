import pytest

def test_post_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_with_empty_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", json={})
    assert response.status_code == 400
    assert response.json()["detail"] == "Request body must not be empty"

def test_post_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", json={"name": None})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid input"

def test_post_with_invalid_data_type(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", json={"key": 123})
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid input type"

def test_post_with_additional_keys(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", json={"key": "value", "extra": "data"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "extra": "data", "name": "post"}