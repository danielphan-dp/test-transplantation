import json
import pytest

def test_post_method_with_empty_kwargs(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/media_range", json={})
    assert response.status_code == 201, response.text
    assert response.json == {'name': 'post'}, response.text

def test_post_method_with_additional_kwargs(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/media_range", json={'extra': 'data'})
    assert response.status_code == 201, response.text
    assert response.json == {'name': 'post', 'extra': 'data'}, response.text

def test_post_method_with_no_kwargs(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/media_range")
    assert response.status_code == 201, response.text
    assert response.json == {'name': 'post'}, response.text

def test_post_method_with_invalid_json(schema_app):
    app_client = schema_app.test_client()
    response = app_client.post("/v1.0/media_range", data='invalid json')
    assert response.status_code == 400, response.text

def test_post_method_with_large_payload(schema_app):
    app_client = schema_app.test_client()
    large_payload = {'key': 'value' * 1000}
    response = app_client.post("/v1.0/media_range", json=large_payload)
    assert response.status_code == 201, response.text
    assert response.json == {'name': 'post', **large_payload}, response.text