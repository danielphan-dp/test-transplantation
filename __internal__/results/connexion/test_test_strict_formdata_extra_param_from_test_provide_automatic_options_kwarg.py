import pytest

def test_post_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={"key1": "value1", "key2": "value2"})
    assert resp.status_code == 201
    assert resp.json() == {"key1": "value1", "key2": "value2", "name": "post"}

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", data="invalid_data")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid input data"

def test_post_with_missing_required_param(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={"key2": "value2"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Missing required parameter 'key1'"