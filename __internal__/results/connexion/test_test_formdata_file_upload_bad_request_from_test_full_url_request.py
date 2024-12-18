import pytest

def test_post_method_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_method_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"extra": "data"})
    assert resp.status_code == 201
    assert resp.json() == {"extra": "data", "name": "post"}

def test_post_method_with_invalid_content_type(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data="invalid data", headers={"Content-Type": "text/plain"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid content type"

def test_post_method_with_missing_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Missing request body"