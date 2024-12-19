import json
import struct
import pytest
from connexion import FlaskApp
from connexion.frameworks.flask import FlaskJSONProvider
from conftest import build_app_from_fixture

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/blob-response?param1=value1&param2=value2")
    assert resp.status_code == 200
    content = resp.data
    assert isinstance(content, bytes)

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/blob-response")
    assert resp.status_code == 200
    content = resp.data
    assert content == b'[{"name": "get"}]'

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/blob-response?param=")
    assert resp.status_code == 200
    content = resp.data
    assert content == b'[{"name": "get"}]'

def test_get_with_none_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/blob-response?param=None")
    assert resp.status_code == 200
    content = resp.data
    assert content == b'[{"name": "get"}]'