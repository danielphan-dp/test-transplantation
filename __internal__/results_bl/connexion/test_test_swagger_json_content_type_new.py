import json
import unittest.mock
import pytest
import connexion

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get('/v1.0/some_endpoint', query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get('/v1.0/some_endpoint')
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get('/v1.0/some_endpoint', query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]