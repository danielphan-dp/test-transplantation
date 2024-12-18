import pytest

def test_post_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={"key": "value"})
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "name": "post"}

def test_post_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={})
    assert resp.status_code == 201
    assert resp.json() == {"name": "post"}

def test_post_method_with_additional_parameters(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={"key": "value", "extra_key": "extra_value"})
    assert resp.status_code == 201
    assert resp.json() == {"key": "value", "extra_key": "extra_value", "name": "post"}

def test_post_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", data="invalid json")
    assert resp.status_code == 400
    assert "Invalid JSON" in resp.json()["detail"]  # Assuming the API returns this detail for invalid JSON

def test_post_method_with_missing_parameters(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/post-endpoint", json={"missing_key": "value"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Missing required parameter(s)"  # Assuming the API returns this detail for missing parameters