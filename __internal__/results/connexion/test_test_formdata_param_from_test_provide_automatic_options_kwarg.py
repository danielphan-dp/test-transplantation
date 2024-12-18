import pytest

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method", json={"key": "value"})
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"key": "value", "name": "post"}

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post"}

def test_post_method_with_multiple_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method", json={"foo": "bar", "baz": "qux"})
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"foo": "bar", "baz": "qux", "name": "post"}

def test_post_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method", data="invalid data")
    assert resp.status_code == 400  # Assuming the endpoint should return 400 for invalid data

def test_post_method_with_large_payload(simple_app):
    app_client = simple_app.test_client()
    large_payload = {f"key_{i}": f"value_{i}" for i in range(1000)}
    resp = app_client.post("/v1.0/post-method", json=large_payload)
    assert resp.status_code == 201
    response = resp.json()
    assert response == {**large_payload, "name": "post"}