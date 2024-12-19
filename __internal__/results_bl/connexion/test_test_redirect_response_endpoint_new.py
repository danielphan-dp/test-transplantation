import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_app):
    result = simple_app.get(name='test')
    assert result == {'name': 'get', 'name': 'test'}

def test_get_without_kwargs(simple_app):
    result = simple_app.get()
    assert result == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    result = simple_app.get(**{})
    assert result == {'name': 'get'}

def test_get_with_multiple_kwargs(simple_app):
    result = simple_app.get(param1='value1', param2='value2')
    assert result == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}