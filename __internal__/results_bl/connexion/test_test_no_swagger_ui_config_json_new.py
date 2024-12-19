import json
import unittest.mock
import pytest
import yaml
from connexion import App

def test_get_with_kwargs():
    app = App(__name__)
    app_client = app.test_client()
    response = app.get(name='test_name')
    assert response == {'name': 'test_name'}

def test_get_without_kwargs():
    app = App(__name__)
    app_client = app.test_client()
    response = app.get()
    assert response == [{'name': 'get'}]

def test_get_with_empty_kwargs():
    app = App(__name__)
    app_client = app.test_client()
    response = app.get(**{})
    assert response == [{'name': 'get'}]

def test_get_with_multiple_kwargs():
    app = App(__name__)
    app_client = app.test_client()
    response = app.get(param1='value1', param2='value2')
    assert response == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}