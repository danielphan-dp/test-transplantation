import pytest

def test_post_method_with_valid_kwargs(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post("/v1.0/post_method", headers=headers, json={"key1": "value1", "key2": "value2"})
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["key1"] == "value1"
    assert response_data["key2"] == "value2"
    assert response_data["name"] == "post"

def test_post_method_with_empty_kwargs(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post("/v1.0/post_method", headers=headers, json={})
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == "post"

def test_post_method_with_invalid_data(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post("/v1.0/post_method", headers=headers, json={"invalid_key": "value"})
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == "post"