import pytest

def test_post_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    body = {"name": "test_name", "tag": "test_tag"}
    resp = app_client.post("/v1.0/post-endpoint", json=body)
    assert resp.status_code == 201
    response = resp.json()
    assert response["name"] == "test_name"
    assert response["tag"] == "test_tag"

def test_post_method_with_missing_name(simple_app):
    app_client = simple_app.test_client()
    body = {"tag": "test_tag"}
    resp = app_client.post("/v1.0/post-endpoint", json=body)
    assert resp.status_code == 400
    response = resp.json()
    assert "name" in response["detail"]

def test_post_method_with_additional_properties(simple_app):
    app_client = simple_app.test_client()
    body = {"name": "test_name", "tag": "test_tag", "extra_property": "extra_value"}
    resp = app_client.post("/v1.0/post-endpoint", json=body)
    assert resp.status_code == 400
    response = resp.json()
    assert "Additional properties are not allowed" in response["detail"]

def test_post_method_with_empty_body(simple_app):
    app_client = simple_app.test_client()
    body = {}
    resp = app_client.post("/v1.0/post-endpoint", json=body)
    assert resp.status_code == 400
    response = resp.json()
    assert "name" in response["detail"]