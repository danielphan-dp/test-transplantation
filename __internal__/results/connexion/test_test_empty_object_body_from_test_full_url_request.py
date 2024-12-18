import pytest

def test_post_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"key": "value"})
    assert resp.status_code == 201
    response = resp.json()
    assert response["key"] == "value"
    assert response["name"] == "post"

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={})
    assert resp.status_code == 201
    response = resp.json()
    assert response == {"name": "post"}

def test_post_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"extra": "data"})
    assert resp.status_code == 201
    response = resp.json()
    assert response["extra"] == "data"
    assert response["name"] == "post"

def test_post_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json="invalid_data")
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for invalid JSON

def test_post_with_none_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json=None)
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for None input