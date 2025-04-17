import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get?param1=value1&param2=value2")
    assert resp.status_code == 200
    assert resp.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get")
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get?param1=")
    assert resp.status_code == 200
    assert resp.json == {'name': 'get', 'param1': ''}

def test_get_with_invalid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get?invalid_param=value")
    assert resp.status_code == 200
    assert 'invalid_param' not in resp.json

def test_get_with_multiple_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get?param1=value1&param2=value2&param3=value3")
    assert resp.status_code == 200
    assert resp.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2', 'param3': 'value3'}