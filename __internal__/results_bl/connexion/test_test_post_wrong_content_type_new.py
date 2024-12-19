import json
import struct
import yaml
from connexion import FlaskApp
from connexion.frameworks.flask import FlaskJSONProvider
from conftest import build_app_from_fixture

def test_post_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        headers={"content-type": "application/json"},
        json={"key": "value"},
    )
    assert resp.status_code == 201
    assert resp.json == {'name': 'post', 'key': 'value'}

def test_post_empty_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        headers={"content-type": "application/json"},
        json={},
    )
    assert resp.status_code == 201
    assert resp.json == {'name': 'post'}

def test_post_invalid_json_structure(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        headers={"content-type": "application/json"},
        json="invalid json",
    )
    assert resp.status_code == 400, "Should return 400 for invalid JSON structure"

def test_post_missing_content_type(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/post",
        json={"key": "value"},
    )
    assert resp.status_code == 415, "Should return 415 when Content-Type is missing"