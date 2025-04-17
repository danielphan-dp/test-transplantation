import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-parameters?param1=value1&param2=value2")
    assert resp.json() == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-parameters")
    assert resp.json() == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-parameters?param1=")
    assert resp.json() == {'name': 'get', 'param1': ''}

def test_get_method_with_none_value(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-parameters?param1=null")
    assert resp.json() == {'name': 'get', 'param1': 'null'}

def test_get_method_with_special_characters(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-parameters?param1=%20&param2=%40")
    assert resp.json() == {'name': 'get', 'param1': ' ', 'param2': '@'}