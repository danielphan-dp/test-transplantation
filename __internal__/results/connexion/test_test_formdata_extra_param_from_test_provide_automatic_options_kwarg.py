import pytest

def test_post_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"key1": "value1", "key2": "value2"})
    assert resp.status_code == 201
    assert resp.json() == {"key1": "value1", "key2": "value2", "name": "post"}

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_with_additional_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"extra_param": "extra_value"})
    assert resp.status_code == 201
    assert resp.json() == {"extra_param": "extra_value", "name": "post"}

def test_post_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json="invalid_data")
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

def test_post_with_large_payload(simple_app):
    app_client = simple_app.test_client()
    large_payload = {f"key{i}": f"value{i}" for i in range(1000)}
    resp = app_client.post("/v1.0/test-post", json=large_payload)
    assert resp.status_code == 201
    assert resp.json() == {**large_payload, "name": "post"}