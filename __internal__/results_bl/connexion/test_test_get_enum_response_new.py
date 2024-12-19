import json
import pytest
from connexion import FlaskApp
from connexion.frameworks.flask import FlaskJSONProvider
from conftest import build_app_from_fixture

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    app.add_api('api.yaml')
    return app

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_enum_response?param1=value1&param2=value2")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert 'name' in data
    assert data['name'] == 'get'

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_enum_response")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'get'

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_enum_response?")
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['name'] == 'get'