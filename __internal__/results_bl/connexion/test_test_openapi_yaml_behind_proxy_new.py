import json
import struct
import yaml
from connexion.FlaskApp import FlaskApp
from connexion.frameworks.flask.FlaskJSONProvider import FlaskJSONProvider
from conftest import build_app_from_fixture
import pytest

def test_get_method_with_kwargs():
    app = FlaskApp(__name__)
    result = app.get(name='test')
    assert result == {'name': 'get', 'name': 'test'}

def test_get_method_without_kwargs():
    app = FlaskApp(__name__)
    result = app.get()
    assert result == [{'name': 'get'}]

def test_get_method_with_empty_kwargs():
    app = FlaskApp(__name__)
    result = app.get(**{})
    assert result == [{'name': 'get'}]

def test_get_method_with_multiple_kwargs():
    app = FlaskApp(__name__)
    result = app.get(param1='value1', param2='value2')
    assert result == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}