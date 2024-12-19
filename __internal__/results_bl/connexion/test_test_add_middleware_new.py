import pytest
from unittest.mock import Mock
from connexion import FlaskApp

@pytest.fixture
def app_class():
    return FlaskApp

def test_get_with_kwargs(app_class):
    app = app_class(__name__)
    result = app.get(name='test')
    assert result == {'name': 'get', 'name': 'test'}

def test_get_without_kwargs(app_class):
    app = app_class(__name__)
    result = app.get()
    assert result == [{'name': 'get'}]

def test_get_with_empty_kwargs(app_class):
    app = app_class(__name__)
    result = app.get()
    assert result == [{'name': 'get'}]

def test_get_with_multiple_kwargs(app_class):
    app = app_class(__name__)
    result = app.get(name='test', value='example')
    assert result == {'name': 'get', 'name': 'test', 'value': 'example'}