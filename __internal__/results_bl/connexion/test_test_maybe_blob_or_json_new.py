import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/binary-response?param1=value1&param2=value2")
    
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/binary-response")
    
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/binary-response?param1=")
    
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'param1': ''}