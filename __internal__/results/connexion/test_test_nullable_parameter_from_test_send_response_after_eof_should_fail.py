import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with a single keyword argument
    resp = app_client.get("/v1.0/get-kwargs?arg1=value1")
    assert resp.json() == {'name': 'get', 'arg1': 'value1'}

    # Test with multiple keyword arguments
    resp = app_client.get("/v1.0/get-kwargs?arg1=value1&arg2=value2")
    assert resp.json() == {'name': 'get', 'arg1': 'value1', 'arg2': 'value2'}

    # Test with no keyword arguments
    resp = app_client.get("/v1.0/get-kwargs")
    assert resp.json() == [{'name': 'get'}]

    # Test with an empty string as a keyword argument
    resp = app_client.get("/v1.0/get-kwargs?arg1=")
    assert resp.json() == {'name': 'get', 'arg1': ''}

    # Test with a None-like value
    resp = app_client.get("/v1.0/get-kwargs?arg1=null")
    assert resp.json() == {'name': 'get', 'arg1': 'null'}

    # Test with a numeric value
    resp = app_client.get("/v1.0/get-kwargs?arg1=123")
    assert resp.json() == {'name': 'get', 'arg1': '123'}