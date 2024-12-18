import pytest

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", json={"key1": "value1", "key2": "value2"})
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"key1": "value1", "key2": "value2", "name": "post"}

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", json={})
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post"}

def test_post_method_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", json={"extra_key": "extra_value"})
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"extra_key": "extra_value", "name": "post"}