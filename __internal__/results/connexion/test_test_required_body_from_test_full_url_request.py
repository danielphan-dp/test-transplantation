import pytest

def test_post_with_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", headers={"content-type": "application/json"})
    assert resp.status_code == 200
    assert resp.json() == {'name': 'post'}

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={})
    assert resp.status_code == 200
    assert resp.json() == {'name': 'post'}

def test_post_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"foo": "bar", "baz": "qux"})
    assert resp.status_code == 200
    assert resp.json() == {'name': 'post', 'foo': 'bar', 'baz': 'qux'}

def test_post_with_invalid_content_type(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data="invalid data", content_type="text/plain")
    assert resp.status_code == 400

def test_post_with_missing_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", headers={"content-type": "application/json"})
    assert resp.status_code == 400