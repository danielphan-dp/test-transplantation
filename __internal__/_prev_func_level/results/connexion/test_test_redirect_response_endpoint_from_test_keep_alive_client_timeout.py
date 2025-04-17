import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key": "value"}, {"key": "value", "name": "get"}),
    ({}, [{"name": "get"}]),
    ({"another_key": "another_value"}, {"another_key": "another_value", "name": "get"}),
])
def test_get_method_with_kwargs(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-method", query_string=kwargs)
    assert resp.json == expected

def test_get_method_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-method")
    assert resp.json == [{"name": "get"}]