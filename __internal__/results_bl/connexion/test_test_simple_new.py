import pytest

def test_get_with_kwargs(swagger_ui_app):
    app_client = swagger_ui_app.test_client()
    response = app_client.get("/v1.0/spec.json", query_string={'key': 'value'})
    assert response.status_code == 200
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(swagger_ui_app):
    app_client = swagger_ui_app.test_client()
    response = app_client.get("/v1.0/spec.json")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(swagger_ui_app):
    app_client = swagger_ui_app.test_client()
    response = app_client.get("/v1.0/spec.json", query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]