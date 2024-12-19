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

def test_post_with_missing_key(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data={"another_key": "test"})
    assert resp.status_code == 201
    assert resp.json == {'another_key': 'test', 'name': 'post'}

def test_post_with_non_string_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", data={"number": 123})
    assert resp.status_code == 201
    assert resp.json == {'number': 123, 'name': 'post'}