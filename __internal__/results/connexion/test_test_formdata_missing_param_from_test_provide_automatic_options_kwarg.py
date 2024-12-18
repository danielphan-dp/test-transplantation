import pytest

def test_post_with_valid_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"param1": "value1", "param2": "value2"})
    assert resp.status_code == 201
    assert resp.json() == {"param1": "value1", "param2": "value2", "name": "post"}

def test_post_with_missing_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"param1": "value1"})
    assert resp.status_code == 201
    assert resp.json() == {"param1": "value1", "name": "post"}

def test_post_with_no_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post")
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data="invalid_json")
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

def test_post_with_additional_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"param1": "value1", "extra_param": "extra_value"})
    assert resp.status_code == 201
    assert resp.json() == {"param1": "value1", "name": "post"}  # Check if extra_param is ignored

def test_post_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}