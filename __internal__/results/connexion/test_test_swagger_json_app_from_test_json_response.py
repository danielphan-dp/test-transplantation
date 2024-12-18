import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_get_with_kwargs(app):
    response = app.get('/v1.0/test', name='example')
    assert response['name'] == 'get'
    assert response['name'] == 'example'

def test_get_without_kwargs(app):
    response = app.get('/v1.0/test')
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]['name'] == 'get'

def test_get_with_empty_kwargs(app):
    response = app.get('/v1.0/test', **{})
    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0]['name'] == 'get'