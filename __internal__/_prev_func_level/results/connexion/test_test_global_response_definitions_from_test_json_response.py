import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method(schema_app, kwargs, expected):
    app_client = schema_app.test_client()
    resp = app_client.get("/v1.0/get", query_string=kwargs)
    assert resp.json() == expected

def test_get_method_no_kwargs(schema_app):
    app_client = schema_app.test_client()
    resp = app_client.get("/v1.0/get")
    assert resp.json() == [{"name": "get"}]