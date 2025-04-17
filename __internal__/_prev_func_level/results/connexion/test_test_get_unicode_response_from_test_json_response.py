import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key": "value"}, {"name": "get", "key": "value"}),
    ({}, [{"name": "get"}]),
    ({"extra": "data"}, {"name": "get", "extra": "data"}),
])
def test_get_method(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string=kwargs)
    assert resp.json() == expected

def test_get_method_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get")
    expected = [{"name": "get"}]
    assert resp.json() == expected

def test_get_method_with_unicode(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string={"currency": "\xa3", "key": "leena"})
    expected = {"name": "get", "currency": "\xa3", "key": "leena"}
    assert resp.json() == expected