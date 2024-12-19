import json
import struct.unpack
import yaml
from connexion.FlaskApp import FlaskApp
from connexion.frameworks.flask.FlaskJSONProvider import FlaskJSONProvider
from conftest import build_app_from_fixture

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_bad_default_response/200?param1=value1&param2=value2")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['name'] == 'get'
    assert data['param1'] == 'value1'
    assert data['param2'] == 'value2'

def test_get_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_bad_default_response/200")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data == [{'name': 'get'}]

def test_get_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_bad_default_response/200?param=value")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['name'] == 'get'
    assert 'param' not in data

def test_get_with_invalid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_bad_default_response/200?invalid_param=value")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data['name'] == 'get'
    assert 'invalid_param' not in data