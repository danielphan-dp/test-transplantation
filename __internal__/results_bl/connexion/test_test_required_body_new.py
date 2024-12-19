import json
import pytest
from connexion import FlaskApp

@pytest.fixture
def simple_app():
    app = FlaskApp(__name__)
    return app

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-required-body", json={})
    assert resp.status_code == 200
    assert resp.json == {'name': 'post'}

def test_post_with_additional_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-required-body", json={"foo": "bar", "baz": "qux"})
    assert resp.status_code == 200
    assert resp.json == {'name': 'post', 'foo': 'bar', 'baz': 'qux'}

def test_post_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-required-body", data="invalid json")
    assert resp.status_code == 400

def test_post_with_missing_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-required-body")
    assert resp.status_code == 400

def test_post_with_none_body(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-required-body", json=None)
    assert resp.status_code == 400