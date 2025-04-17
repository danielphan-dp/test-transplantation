import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get('/v1.0/test_get?param1=value1&param2=value2')
    assert response.json() == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get('/v1.0/test_get')
    assert response.json() == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get('/v1.0/test_get?empty_param=')
    assert response.json() == {'name': 'get', 'empty_param': ''}

def test_get_with_special_characters(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get('/v1.0/test_get?param1=%20%21%22%23%24%25%26%27%28%29')
    assert response.json() == {'name': 'get', 'param1': ' !"#$%&\'()'}

def test_get_with_numeric_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get('/v1.0/test_get?param1=123&param2=456')
    assert response.json() == {'name': 'get', 'param1': '123', 'param2': '456'}