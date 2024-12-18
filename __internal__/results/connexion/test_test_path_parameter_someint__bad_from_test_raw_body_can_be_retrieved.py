import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({"key1": "value1", "key2": "value2"}, {"key1": "value1", "key2": "value2", "name": "get"}),
])
def test_get_with_kwargs(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string=kwargs)
    assert resp.json == expected, resp.text

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get")
    assert resp.json == [{'name': 'get'}], resp.text

def test_get_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string={})
    assert resp.json == [{'name': 'get'}], resp.text

def test_get_with_invalid_route(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/invalid-route")
    assert resp.status_code == 404, resp.text