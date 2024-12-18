import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_get_with_kwargs(app):
    response = app.get(name='test')
    assert response == {'name': 'get', 'name': 'test'}

def test_get_without_kwargs(app):
    response = app.get()
    assert response == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    response = app.get(**{})
    assert response == [{'name': 'get'}]

def test_get_with_multiple_kwargs(app):
    response = app.get(name='test', type='example')
    assert response == {'name': 'get', 'name': 'test', 'type': 'example'}