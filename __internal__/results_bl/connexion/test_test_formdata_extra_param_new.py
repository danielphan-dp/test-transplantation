import json
import pytest

def test_post_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data={"key": "value"})
    assert resp.status_code == 201
    assert resp.json == {'key': 'value', 'name': 'post'}

def test_post_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data={})
    assert resp.status_code == 201
    assert resp.json == {'name': 'post'}

def test_post_with_additional_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data={"key": "value", "extra_key": "extra_value"})
    assert resp.status_code == 201
    assert resp.json == {'key': 'value', 'extra_key': 'extra_value', 'name': 'post'}

def test_post_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data={"key": None})
    assert resp.status_code == 201
    assert resp.json == {'key': None, 'name': 'post'}