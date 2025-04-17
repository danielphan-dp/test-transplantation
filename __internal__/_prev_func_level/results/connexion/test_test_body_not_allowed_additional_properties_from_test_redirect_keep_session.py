import pytest

def test_post_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    body = {"key1": "value1", "key2": "value2"}
    resp = app_client.post(
        "/v1.0/post-endpoint",
        json=body,
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"key1": "value1", "key2": "value2", "name": "post"}

def test_post_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    body = {}
    resp = app_client.post(
        "/v1.0/post-endpoint",
        json=body,
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post"}

def test_post_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    body = {"invalid_key": "invalid_value"}
    resp = app_client.post(
        "/v1.0/post-endpoint",
        json=body,
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"invalid_key": "invalid_value", "name": "post"}

def test_post_method_with_additional_properties(simple_app):
    app_client = simple_app.test_client()
    body = {"name": "test", "extra_property": "extra_value"}
    resp = app_client.post(
        "/v1.0/post-endpoint",
        json=body,
    )
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post", "extra_property": "extra_value"}