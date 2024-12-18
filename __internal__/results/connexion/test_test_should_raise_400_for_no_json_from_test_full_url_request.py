import pytest

def test_post_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", json={"other_key": "value"})
    assert response.status_code == 201
    assert response.json() == {"other_key": "value", "name": "post"}

def test_post_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-endpoint", data="invalid json")
    assert response.status_code == 400
    assert response.json()["detail"] == "Request body must be valid JSON"