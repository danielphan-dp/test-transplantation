import json
import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.get("/v1.0/test-required-param", params={"key": "value"})
    assert resp.status_code == 200
    assert json.loads(resp.data) == {'name': 'get', 'key': 'value'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.get("/v1.0/test-required-param")
    assert resp.status_code == 200
    assert json.loads(resp.data) == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.get("/v1.0/test-required-param", params={})
    assert resp.status_code == 200
    assert json.loads(resp.data) == [{'name': 'get'}]

def test_get_method_with_multiple_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.get("/v1.0/test-required-param", params={"key1": "value1", "key2": "value2"})
    assert resp.status_code == 200
    assert json.loads(resp.data) == {'name': 'get', 'key1': 'value1', 'key2': 'value2'}