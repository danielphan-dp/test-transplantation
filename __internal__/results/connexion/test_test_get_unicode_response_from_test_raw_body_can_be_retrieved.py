import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string={"key": "value"})
    expected_json = {"key": "value", "name": "get"}
    assert resp.json() == expected_json

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get")
    expected_json = [{"name": "get"}]
    assert resp.json() == expected_json

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string={})
    expected_json = [{"name": "get"}]
    assert resp.json() == expected_json

def test_get_with_multiple_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string={"key1": "value1", "key2": "value2"})
    expected_json = {"key1": "value1", "key2": "value2", "name": "get"}
    assert resp.json() == expected_json

def test_get_with_unicode_key(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string={"currency": "\xa3"})
    expected_json = {"currency": "\xa3", "name": "get"}
    assert resp.json() == expected_json