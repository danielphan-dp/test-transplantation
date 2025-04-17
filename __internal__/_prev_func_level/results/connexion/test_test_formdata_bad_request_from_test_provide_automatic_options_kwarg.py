import pytest

def test_post_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json={"extra": "data"})
    assert resp.status_code == 201
    assert resp.json() == {"extra": "data", "name": "post"}

def test_post_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post", json="invalid_data")
    assert resp.status_code == 400
    response = resp.json()
    assert response["detail"] == "Invalid JSON data"  # Assuming the API returns this for invalid JSON

def test_post_without_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post")
    assert resp.status_code == 400
    response = resp.json()
    assert response["detail"] == "Missing JSON body"  # Assuming the API returns this for missing JSON body