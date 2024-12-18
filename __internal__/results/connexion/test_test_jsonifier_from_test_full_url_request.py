import pytest

def test_post_method_with_valid_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/post", json={"key": "value"})
    assert response.status_code == 201
    assert response.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {"name": "post"}

def test_post_method_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/post", json={"extra": "data"})
    assert response.status_code == 201
    assert response.json() == {"extra": "data", "name": "post"}

def test_post_method_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/post", data="invalid data")
    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid data

def test_post_method_with_large_payload(simple_app):
    app_client = simple_app.test_client()
    large_payload = {"key": "value" * 1000}
    response = app_client.post("/v1.0/post", json=large_payload)
    assert response.status_code == 201
    assert response.json() == {**large_payload, "name": "post"}