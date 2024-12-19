import json
import struct.unpack
import yaml
from connexion.FlaskApp import FlaskApp
from connexion.frameworks.flask.FlaskJSONProvider import FlaskJSONProvider
from conftest import build_app_from_fixture

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test_with_kwargs?key=value")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'key': 'value'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test_without_kwargs")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test_with_empty_kwargs?key=")
    assert response.status_code == 200
    assert response.json == {'name': 'get', 'key': ''}