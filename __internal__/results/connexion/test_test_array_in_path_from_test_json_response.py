import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string={"key": "value"})
    assert resp.json() == {"key": "value", "name": "get"}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get")
    assert resp.json() == [{"name": "get"}]

def test_get_with_multiple_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string={"key1": "value1", "key2": "value2"})
    assert resp.json() == {"key1": "value1", "key2": "value2", "name": "get"}

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string={})
    assert resp.json() == [{"name": "get"}]