import json
import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-int-path", query_string={'key': 'value'})
    assert resp.status_code == 200
    assert json.loads(resp.data) == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-int-path")
    assert resp.status_code == 200
    assert json.loads(resp.data) == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-int-path", query_string={})
    assert resp.status_code == 200
    assert json.loads(resp.data) == [{'name': 'get'}]