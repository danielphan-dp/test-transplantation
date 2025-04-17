import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    kwargs = {'key1': 'value1', 'key2': 'value2'}
    
    resp = app_client.get("/v1.0/get", query_string=kwargs)
    assert resp.status_code == 200
    assert resp.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.get("/v1.0/get")
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    kwargs = {}
    
    resp = app_client.get("/v1.0/get", query_string=kwargs)
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]