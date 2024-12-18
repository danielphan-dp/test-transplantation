import pytest

def test_post_method_with_valid_data(secure_api_app):
    app_client = secure_api_app.test_client()
    headers = {"Authorization": "Bearer 100"}
    response = app_client.post("/v1.0/greeting/rcaricio", json={"key": "value"}, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_without_auth(secure_api_app):
    app_client = secure_api_app.test_client()
    response = app_client.post("/v1.0/greeting/rcaricio", json={"key": "value"})
    assert response.status_code == 401

def test_post_method_with_invalid_auth(secure_api_app):
    app_client = secure_api_app.test_client()
    headers = {"Authorization": "Bearer invalid"}
    response = app_client.post("/v1.0/greeting/rcaricio", json={"key": "value"}, headers=headers)
    assert response.status_code == 401

def test_post_method_with_empty_body(secure_api_app):
    app_client = secure_api_app.test_client()
    headers = {"Authorization": "Bearer 100"}
    response = app_client.post("/v1.0/greeting/rcaricio", json={}, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_missing_key(secure_api_app):
    app_client = secure_api_app.test_client()
    headers = {"Authorization": "Bearer 100"}
    response = app_client.post("/v1.0/greeting/rcaricio", json={"other_key": "value"}, headers=headers)
    assert response.status_code == 201
    assert response.json() == {"other_key": "value", "name": "post"}