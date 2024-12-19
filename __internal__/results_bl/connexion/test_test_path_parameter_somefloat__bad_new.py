import json
import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-get-path", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200
    assert json.loads(response.data) == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-get-path")
    assert response.status_code == 200
    assert json.loads(response.data) == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-get-path", query_string={})
    assert response.status_code == 200
    assert json.loads(response.data) == [{'name': 'get'}]