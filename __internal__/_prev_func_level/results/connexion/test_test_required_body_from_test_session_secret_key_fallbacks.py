import pytest

def test_post_method_with_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

def test_post_method_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", json={"foo": "bar"})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'foo': 'bar'}

def test_post_method_with_invalid_content_type(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", data="foo=bar", content_type="application/x-www-form-urlencoded")
    assert resp.status_code == 400

def test_post_method_with_missing_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", headers={"content-type": "application/json"})
    assert resp.status_code == 400