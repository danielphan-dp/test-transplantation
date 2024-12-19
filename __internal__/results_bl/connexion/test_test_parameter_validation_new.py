import json
import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    url = "/v1.0/get_method"

    response = app_client.get(url, params={"key1": "value1", "key2": "value2"})
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'key1': 'value1', 'key2': 'value2'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    url = "/v1.0/get_method"

    response = app_client.get(url)
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    url = "/v1.0/get_method"

    response = app_client.get(url, params={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_method_with_invalid_kwargs(simple_app):
    app_client = simple_app.test_client()
    url = "/v1.0/get_method"

    response = app_client.get(url, params={"invalid_key": None})
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'invalid_key': None}