import json
import unittest.mock
import pytest
import yaml
from connexion import App

def test_get_with_kwargs(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app_client = app.test_client()
    url = "/v1.0/{spec}"
    url = url.format(spec=spec)
    
    response = app_client.get(url, query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app_client = app.test_client()
    url = "/v1.0/{spec}"
    url = url.format(spec=spec)
    
    response = app_client.get(url)
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app_client = app.test_client()
    url = "/v1.0/{spec}"
    url = url.format(spec=spec)
    
    response = app_client.get(url, query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]