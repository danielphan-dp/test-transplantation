import pytest

def test_get_with_kwargs(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    kwargs = {'key1': 'value1', 'key2': 'value2'}
    response = app_client.get("/v1.0/get", query_string=kwargs)
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

def test_get_without_kwargs(schema_app):
    app_client = schema_app.test_client()
    headers = {"Content-type": "application/json"}

    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    assert response.headers.get("content-type") == "application/json"
    assert response.json == [{'name': 'get'}]