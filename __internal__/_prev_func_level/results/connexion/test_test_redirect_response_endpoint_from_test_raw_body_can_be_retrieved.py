import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key": "value"}, {"key": "value", "name": "get"}),
    ({}, [{"name": "get"}]),
])
def test_get_method(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method", query_string=kwargs)
    assert resp.json == expected
    assert resp.status_code == 200

def test_get_method_with_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method")
    assert resp.json == [{"name": "get"}]
    assert resp.status_code == 200

def test_get_method_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method", query_string={})
    assert resp.json == [{"name": "get"}]
    assert resp.status_code == 200

def test_get_method_with_multiple_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method", query_string={"key1": "value1", "key2": "value2"})
    assert resp.json == {"key1": "value1", "key2": "value2", "name": "get"}
    assert resp.status_code == 200