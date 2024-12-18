import pytest
from io import BytesIO

def test_post_method_with_kwargs(simple_app):
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

def test_post_method_with_large_data(simple_app):
    app_client = simple_app.test_client()
    large_data = {"key": "x" * 10000}
    resp = app_client.post("/v1.0/test-post", json=large_data)
    
    assert resp.status_code == 201
    assert resp.json() == {"key": "x" * 10000, "name": "post"}