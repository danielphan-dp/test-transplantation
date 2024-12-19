import json
import unittest.mock
import pytest
import connexion

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/async-route?param1=value1&param2=value2")
    assert resp.status_code == 200
    assert resp.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/async-route")
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/async-route?")
    assert resp.status_code == 200
    assert resp.json == [{'name': 'get'}]