import json
import pytest

def test_get_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string={'key1': 'value1', 'key2': 'value2'})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.get("/v1.0/test-get")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string={})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data == [{'name': 'get'}]