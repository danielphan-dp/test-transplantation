import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method", query_string={'key': 'value'})
    assert resp.json == {'key': 'value', 'name': 'get'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method")
    assert resp.json == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method", query_string={})
    assert resp.json == [{'name': 'get'}]