import json
import unittest.mock
import pytest
import connexion

@pytest.fixture
def simple_app():
    app = connexion.App(__name__)
    return app

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method?key=value")
    assert resp.json == {'name': 'get', 'key': 'value'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method")
    assert resp.json == [{'name': 'get'}]

def test_get_method_with_multiple_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method?key1=value1&key2=value2")
    assert resp.json == {'name': 'get', 'key1': 'value1', 'key2': 'value2'}

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/method?")
    assert resp.json == [{'name': 'get'}]