import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    response_with_kwargs = app_client.get("/v1.0/get", query_string={"key": "value"})
    assert response_with_kwargs.status_code == 200
    assert response_with_kwargs.headers.get("content-type") == "application/json"
    response_data = response_with_kwargs.json()
    assert response_data["key"] == "value"
    assert response_data["name"] == "get"

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    response_without_kwargs = app_client.get("/v1.0/get")
    assert response_without_kwargs.status_code == 200
    assert response_without_kwargs.headers.get("content-type") == "application/json"
    response_data = response_without_kwargs.json()
    assert len(response_data) == 1
    assert response_data[0]["name"] == "get"