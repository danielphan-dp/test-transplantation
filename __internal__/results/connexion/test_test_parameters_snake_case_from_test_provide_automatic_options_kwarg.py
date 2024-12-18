import json
import pytest

def test_post_method_with_valid_data(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-post-path/123",
        headers=headers,
        json={"key": "value"},
    )
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-post-path/123",
        headers=headers,
        json={},
    )
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_method_with_invalid_data(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-post-path/123",
        headers=headers,
        json={"invalid_key": "value"},
    )
    assert resp.status_code == 201
    assert resp.json() == {"invalid_key": "value", "name": "post"}

def test_post_method_with_non_json_data(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "text/plain"}
    resp = app_client.post(
        "/v1.0/test-post-path/123",
        headers=headers,
        data="This is not JSON",
    )
    assert resp.status_code == 415  # Unsupported Media Type

def test_post_method_with_query_parameters(snake_case_app):
    app_client = snake_case_app.test_client()
    headers = {"Content-type": "application/json"}
    resp = app_client.post(
        "/v1.0/test-post-path/123?param=value",
        headers=headers,
        json={"key": "value"},
    )
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}