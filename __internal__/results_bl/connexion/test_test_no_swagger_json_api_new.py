import json
import unittest.mock
import pytest
from connexion import App

def test_get_with_kwargs():
    app = App(__name__)
    client = app.test_client()
    response = client.get('/v1.0/test', query_string={'key': 'value'})
    assert response.status_code == 200
    assert json.loads(response.data) == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs():
    app = App(__name__)
    client = app.test_client()
    response = client.get('/v1.0/test')
    assert response.status_code == 200
    assert json.loads(response.data) == [{'name': 'get'}]

def test_get_with_empty_kwargs():
    app = App(__name__)
    client = app.test_client()
    response = client.get('/v1.0/test', query_string={})
    assert response.status_code == 200
    assert json.loads(response.data) == [{'name': 'get'}]