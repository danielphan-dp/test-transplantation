import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_get_with_kwargs(app):
    kwargs = {'key1': 'value1', 'key2': 'value2'}
    response = app.get('/v1.0/get', **kwargs)
    assert response.status_code == 200
    assert response.json() == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs(app):
    response = app.get('/v1.0/get')
    assert response.status_code == 200
    assert response.json() == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    kwargs = {}
    response = app.get('/v1.0/get', **kwargs)
    assert response.status_code == 200
    assert response.json() == [{'name': 'get'}]