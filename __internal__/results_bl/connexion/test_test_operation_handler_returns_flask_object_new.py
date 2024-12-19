import pytest
from connexion import FlaskApp

@pytest.fixture
def app():
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(app):
    response = app.get(name='test')
    assert response == {'name': 'get', 'name': 'test'}

def test_get_without_kwargs(app):
    response = app.get()
    assert response == [{'name': 'get'}]

def test_get_with_empty_kwargs(app):
    response = app.get(**{})
    assert response == {'name': 'get'}

def test_get_with_multiple_kwargs(app):
    response = app.get(param1='value1', param2='value2')
    assert response == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}