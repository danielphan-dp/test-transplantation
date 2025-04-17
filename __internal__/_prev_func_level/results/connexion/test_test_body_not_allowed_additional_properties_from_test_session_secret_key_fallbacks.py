import pytest

def test_post_method_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    kwargs = {"key1": "value1", "key2": "value2"}
    resp = app_client.post("/v1.0/post-endpoint", json=kwargs)
    assert resp.status_code == 201
    assert resp.json() == {"key1": "value1", "key2": "value2", "name": "post"}

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    kwargs = {}
    resp = app_client.post("/v1.0/post-endpoint", json=kwargs)
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    kwargs = {"invalid_key": "invalid_value"}
    resp = app_client.post("/v1.0/post-endpoint", json=kwargs)
    assert resp.status_code == 201
    assert resp.json() == {"invalid_key": "invalid_value", "name": "post"}

def test_post_method_with_additional_properties(simple_app):
    app_client = simple_app.test_client()
    kwargs = {"name": "test", "extra_property": "extra_value"}
    resp = app_client.post("/v1.0/post-endpoint", json=kwargs)
    assert resp.status_code == 201
    assert resp.json() == {"name": "post", "extra_property": "extra_value"}