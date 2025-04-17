import pytest
from io import BytesIO

def test_post_method_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_method_with_additional_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", json={"extra": "data"})
    assert resp.status_code == 201
    assert resp.json() == {"extra": "data", "name": "post"}

def test_post_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-post-method", data="invalid data")
    assert resp.status_code == 400  # Assuming the endpoint should return 400 for invalid data

def test_post_method_with_file_upload(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post(
        "/v1.0/test-post-method",
        files={"file": ("example.txt", BytesIO(b"file contents"))},
    )
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}  # Assuming the file upload does not affect the response structure