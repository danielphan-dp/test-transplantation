import json
import struct.unpack
import yaml
from connexion.FlaskApp import FlaskApp
from connexion.frameworks.flask.FlaskJSONProvider import FlaskJSONProvider
from conftest import build_app_from_fixture
import pytest

@pytest.fixture
def valid_operations_app():
    app = FlaskApp(__name__)
    app.add_api('api.yaml')
    return app

def test_post_valid_operations(valid_operations_app):
    app_client = valid_operations_app.test_client()
    resp = app_client.post("/v1.0/welcome", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json == {'name': 'post', 'key': 'value'}

def test_post_empty_payload(valid_operations_app):
    app_client = valid_operations_app.test_client()
    resp = app_client.post("/v1.0/welcome", json={})
    assert resp.status_code == 201
    assert resp.json == {'name': 'post'}

def test_post_invalid_json(valid_operations_app):
    app_client = valid_operations_app.test_client()
    resp = app_client.post("/v1.0/welcome", data="invalid json")
    assert resp.status_code == 400

def test_post_with_additional_params(valid_operations_app):
    app_client = valid_operations_app.test_client()
    resp = app_client.post("/v1.0/welcome", json={"key": "value", "extra": "data"})
    assert resp.status_code == 201
    assert resp.json == {'name': 'post', 'key': 'value', 'extra': 'data'}