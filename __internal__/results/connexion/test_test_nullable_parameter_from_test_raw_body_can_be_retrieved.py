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

    # Test with empty string as a keyword argument
    resp = app_client.get("/v1.0/get-kwargs?arg1=")
    assert resp.json() == {'name': 'get', 'arg1': ''}

    # Test with special characters in keyword arguments
    resp = app_client.get("/v1.0/get-kwargs?arg1=hello%20world")
    assert resp.json() == {'name': 'get', 'arg1': 'hello world'}