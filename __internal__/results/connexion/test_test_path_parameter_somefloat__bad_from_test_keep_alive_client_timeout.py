import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-path", query_string={'key1': 'value1', 'key2': 'value2'})
    assert resp.status_code == 200
    assert resp.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-path")
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-path", query_string={})
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]