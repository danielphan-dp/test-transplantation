import json
import struct
import yaml
from connexion import FlaskApp
from connexion.frameworks.flask import FlaskJSONProvider
from conftest import build_app_from_fixture
import pytest

def test_post_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/text-request", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json == {'key': 'value', 'name': 'post'}

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/text-request", json={})
    assert resp.status_code == 201
    assert resp.json == {'name': 'post'}

def test_post_with_invalid_content_type(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/text-request", data="text", content_type='text/plain')
    assert resp.status_code == 415

def test_post_with_non_json_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/text-request", data="non-json-data")
    assert resp.status_code == 400

def test_post_with_large_payload(simple_app):
    app_client = simple_app.test_client()
    large_payload = {"key": "value" * 1000}
    resp = app_client.post("/v1.0/text-request", json=large_payload)
    assert resp.status_code == 201
    assert resp.json == {**large_payload, 'name': 'post'}