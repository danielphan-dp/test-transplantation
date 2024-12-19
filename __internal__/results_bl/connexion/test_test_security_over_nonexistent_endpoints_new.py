import pytest
from connexion import App

def test_get_method_with_kwargs(secure_api_app):
    app_client = secure_api_app.test_client()
    response = app_client.get("/v1.0/get-endpoint", query_string={'key': 'value'})
    assert response.status_code == 200
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_method_without_kwargs(secure_api_app):
    app_client = secure_api_app.test_client()
    response = app_client.get("/v1.0/get-endpoint")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(secure_api_app):
    app_client = secure_api_app.test_client()
    response = app_client.get("/v1.0/get-endpoint", query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_method_with_multiple_kwargs(secure_api_app):
    app_client = secure_api_app.test_client()
    response = app_client.get("/v1.0/get-endpoint", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}