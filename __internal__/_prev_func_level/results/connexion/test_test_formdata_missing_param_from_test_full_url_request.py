import pytest

def test_post_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_with_additional_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"extra_param": "extra_value"})
    assert resp.status_code == 201
    assert resp.json() == {"extra_param": "extra_value", "name": "post"}

def test_post_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data="invalid_json")
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

def test_post_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"name": "post"})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}  # Testing behavior when 'key' is missing