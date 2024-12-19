import json
import pytest

def test_get_with_kwargs(schema_app):
    app_client = schema_app.test_client()
    response = app_client.get("/v1.0/test_schema/response/object/valid", query_string={'key': 'value'})
    assert response.status_code == 200, response.text
    assert json.loads(response.data) == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(schema_app):
    app_client = schema_app.test_client()
    response = app_client.get("/v1.0/test_schema/response/object/valid")
    assert response.status_code == 200, response.text
    assert json.loads(response.data) == [{'name': 'get'}]

def test_get_with_empty_kwargs(schema_app):
    app_client = schema_app.test_client()
    response = app_client.get("/v1.0/test_schema/response/object/valid", query_string={})
    assert response.status_code == 200, response.text
    assert json.loads(response.data) == [{'name': 'get'}]

def test_get_with_multiple_kwargs(schema_app):
    app_client = schema_app.test_client()
    response = app_client.get("/v1.0/test_schema/response/object/valid", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200, response.text
    assert json.loads(response.data) == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}