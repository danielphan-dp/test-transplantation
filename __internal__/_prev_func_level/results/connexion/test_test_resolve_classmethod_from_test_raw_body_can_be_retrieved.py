import pytest
from connexion import App

@pytest.fixture
def simple_app():
    app = App(__name__)
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/classmethod?arg1=value1&arg2=value2")
    assert resp.json == {'name': 'get', 'arg1': 'value1', 'arg2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/classmethod")
    assert resp.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/resolver-test/classmethod?arg1=")
    assert resp.json == {'name': 'get', 'arg1': ''}