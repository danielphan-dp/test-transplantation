import pytest

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

def test_post_method_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method", json={"extra_param": "value"})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'extra_param': 'value'}

def test_post_method_with_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

def test_post_method_with_varied_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method", json={"key1": "value1", "key2": "value2"})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'key1': 'value1', 'key2': 'value2'}

def test_post_method_with_numeric_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-method", json={"number": 123})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'number': 123}