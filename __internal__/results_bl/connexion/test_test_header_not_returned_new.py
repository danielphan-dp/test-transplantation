import json
import pytest

def test_get_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/goodday", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200
    data = response.json()
    assert data['key1'] == 'value1'
    assert data['key2'] == 'value2'
    assert data['name'] == 'get'

def test_get_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    
    response = app_client.get("/v1.0/goodday")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['name'] == 'get'