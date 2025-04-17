import pytest

def test_get_method_with_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    response = app_client.get("/v1.0/get_method", query_string={"key1": "value1", "key2": "value2"})
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_json = response.json()
    assert response_json["key1"] == "value1"
    assert response_json["key2"] == "value2"
    assert response_json["name"] == "get"

def test_get_method_without_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    response = app_client.get("/v1.0/get_method")
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["name"] == "get"

def test_get_method_with_empty_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()

    response = app_client.get("/v1.0/get_method", query_string={})
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["name"] == "get"