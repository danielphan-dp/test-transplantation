import pytest

def test_get_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method", params={"key": "value"})
    assert resp.status_code == 200
    response = resp.json()
    assert response == {'name': 'get', 'key': 'value'}

def test_get_method_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method")
    assert resp.status_code == 200
    response = resp.json()
    assert response == [{'name': 'get'}]

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method", params={})
    assert resp.status_code == 200
    response = resp.json()
    assert response == [{'name': 'get'}]