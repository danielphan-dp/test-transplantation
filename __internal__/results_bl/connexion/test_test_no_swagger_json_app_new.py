import json
import unittest.mock
import pytest
from connexion import App

def test_get_with_kwargs():
    app = App(__name__)
    app_client = app.test_client()
    
    response = app.get(name='test_name')
    assert response == {'name': 'get', 'name': 'test_name'}

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
    
    response = app.get(name='test_name', extra='extra_value')
    assert response == {'name': 'get', 'name': 'test_name', 'extra': 'extra_value'}