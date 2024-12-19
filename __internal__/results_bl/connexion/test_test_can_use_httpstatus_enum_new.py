import json
import struct
import yaml
from connexion import FlaskApp
from connexion.frameworks.flask import FlaskJSONProvider
from conftest import build_app_from_fixture
import pytest

def test_get_method_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/httpstatus?param1=value1&param2=value2")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_method_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/httpstatus")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/httpstatus?param1=")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'param1': ''}