import pytest

def test_post_method_with_valid_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/post-method",
        json={"key": "value"},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/post-method",
        json={},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post"}

def test_post_method_with_additional_properties(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/post-method",
        json={"extra": "data", "another": 123},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"extra": "data", "another": 123, "name": "post"}

def test_post_method_with_invalid_json(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/post-method",
        data="invalid json",
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 400

def test_post_method_with_missing_content_type(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/post-method",
        json={"key": "value"},
    )
    assert resp.status_code == 415