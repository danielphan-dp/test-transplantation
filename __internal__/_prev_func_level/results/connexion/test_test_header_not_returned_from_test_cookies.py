import pytest

def test_get_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/goodday", query_string={'key': 'value'})
    assert response.status_code == 200
    assert response.json() == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/goodday")
    assert response.status_code == 200
    assert response.json() == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/goodday", query_string={})
    assert response.status_code == 200
    assert response.json() == [{'name': 'get'}]