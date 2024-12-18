import pytest

def test_get_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    response = app_client.get("/v1.0/get_method", query_string={"key": "value"})
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json()
    assert response_data["key"] == "value"
    assert response_data["name"] == "get"

def test_get_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    response = app_client.get("/v1.0/get_method")
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["name"] == "get"

def test_get_with_empty_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    response = app_client.get("/v1.0/get_method", query_string={})
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["name"] == "get"