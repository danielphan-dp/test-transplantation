import pytest

def test_get_with_kwargs(app_client):
    response = app_client.get("/v1.0/welcome", query_string={'key': 'value'})
    assert response.status_code == 200
    assert response.json == {'key': 'value', 'name': 'get'}

def test_get_without_kwargs(app_client):
    response = app_client.get("/v1.0/welcome")
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_empty_kwargs(app_client):
    response = app_client.get("/v1.0/welcome", query_string={})
    assert response.status_code == 200
    assert response.json == [{'name': 'get'}]

def test_get_with_multiple_kwargs(app_client):
    response = app_client.get("/v1.0/welcome", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response.status_code == 200
    assert response.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}