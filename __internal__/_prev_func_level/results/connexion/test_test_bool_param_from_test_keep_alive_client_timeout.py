import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", params={"key1": "value1", "key2": "value2"})
    assert resp.status_code == 200
    response = resp.json()
    assert response == {'name': 'get', 'key1': 'value1', 'key2': 'value2'}

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get")
    assert resp.status_code == 200
    response = resp.json()
    assert response == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", params={})
    assert resp.status_code == 200
    response = resp.json()
    assert response == [{'name': 'get'}]