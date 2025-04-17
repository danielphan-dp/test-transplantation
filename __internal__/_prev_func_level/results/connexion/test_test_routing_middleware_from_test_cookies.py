import pytest

def test_get_with_kwargs(middleware_app):
    app_client = middleware_app.test_client()
    
    response = app_client.get("/v1.0/greeting", query_string={"key": "value"})
    
    assert response.json == {'key': 'value', 'name': 'get'}
    
def test_get_without_kwargs(middleware_app):
    app_client = middleware_app.test_client()
    
    response = app_client.get("/v1.0/greeting")
    
    assert response.json == [{'name': 'get'}]