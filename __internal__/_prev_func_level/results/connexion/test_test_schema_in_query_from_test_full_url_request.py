import pytest

def test_post_method_with_valid_data(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post(
        "/v1.0/post_method",
        headers=headers,
        json={"key": "value"}
    )
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["key"] == "value"
    assert response_data["name"] == "post"

def test_post_method_with_empty_data(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post(
        "/v1.0/post_method",
        headers=headers,
        json={}
    )
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["name"] == "post"

def test_post_method_with_additional_parameters(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}
    
    response = app_client.post(
        "/v1.0/post_method",
        headers=headers,
        json={"extra_param": "extra_value"}
    )
    
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["extra_param"] == "extra_value"
    assert response_data["name"] == "post"