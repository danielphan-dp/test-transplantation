import pytest

def test_post_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodevening/dan", json={"key": "value"})
    assert response.status_code == 201
    assert response.json == {"name": "post", "key": "value"}

def test_post_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodevening/dan", json={})
    assert response.status_code == 201
    assert response.json == {"name": "post"}

def test_post_method_with_additional_parameters(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodevening/dan", json={"extra": "data"})
    assert response.status_code == 201
    assert response.json == {"name": "post", "extra": "data"}

def test_post_method_with_invalid_url(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/nonexistent", json={"key": "value"})
    assert response.status_code == 404

def test_post_method_with_no_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodevening/dan", data="not_json")
    assert response.status_code == 400  # Assuming the server returns a 400 for invalid JSON input