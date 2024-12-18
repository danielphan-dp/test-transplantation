import pytest

def test_post_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={"invalid_key": "value"})
    assert resp.status_code == 201
    assert resp.json() == {"invalid_key": "value", "name": "post"}

def test_post_method_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint")
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}