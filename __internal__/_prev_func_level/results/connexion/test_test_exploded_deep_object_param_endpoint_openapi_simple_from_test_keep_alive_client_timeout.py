import pytest

def test_get_method_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get?foo=bar&baz=qux")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'foo': 'bar', 'baz': 'qux', 'name': 'get'}

def test_get_method_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/get?empty=")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == {'empty': '', 'name': 'get'}