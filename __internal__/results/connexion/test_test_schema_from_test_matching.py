import pytest

def test_get_method_with_kwargs(schema_app):
    app_client = schema_app.test_client()

    response_with_kwargs = app_client.get("/v1.0/get_method", query_string={"key": "value"})
    assert response_with_kwargs.status_code == 200
    response_data = response_with_kwargs.json()
    assert response_data["key"] == "value"
    assert response_data["name"] == "get"

def test_get_method_without_kwargs(schema_app):
    app_client = schema_app.test_client()

    response_without_kwargs = app_client.get("/v1.0/get_method")
    assert response_without_kwargs.status_code == 200
    response_data = response_without_kwargs.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["name"] == "get"

def test_get_method_with_empty_kwargs(schema_app):
    app_client = schema_app.test_client()

    response_with_empty_kwargs = app_client.get("/v1.0/get_method", query_string={})
    assert response_with_empty_kwargs.status_code == 200
    response_data = response_with_empty_kwargs.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]["name"] == "get"

def test_get_method_with_multiple_kwargs(schema_app):
    app_client = schema_app.test_client()

    response_with_multiple_kwargs = app_client.get("/v1.0/get_method", query_string={"key1": "value1", "key2": "value2"})
    assert response_with_multiple_kwargs.status_code == 200
    response_data = response_with_multiple_kwargs.json()
    assert response_data["key1"] == "value1"
    assert response_data["key2"] == "value2"
    assert response_data["name"] == "get"