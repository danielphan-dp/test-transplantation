import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string={'key': 'value'})
    assert resp.status_code == 200
    assert resp.json == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get")
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string={})
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]