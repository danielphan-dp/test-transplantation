import pytest

def test_post_method_with_valid_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post-method",
        json={"key": "value"},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post-method",
        json={},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post"}

def test_post_method_with_invalid_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post-method",
        json={"invalid_key": None},
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"invalid_key": None, "name": "post"}

def test_post_method_with_large_data(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    large_data = {f"key_{i}": f"value_{i}" for i in range(1000)}
    resp = app_client.post(
        "/v1.0/test-post-method",
        json=large_data,
        headers={"Content-Type": "application/json"},
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {**large_data, "name": "post"}