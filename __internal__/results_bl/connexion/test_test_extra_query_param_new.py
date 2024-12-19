import json
import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_parameter_validation?param1=value1&param2=value2"
    resp = app_client.get(url, headers=headers)
    assert resp.status_code == 200
    assert resp.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_parameter_validation"
    resp = app_client.get(url, headers=headers)
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    headers = {"Content-type": "application/json"}
    url = "/v1.0/test_parameter_validation?"
    resp = app_client.get(url, headers=headers)
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]