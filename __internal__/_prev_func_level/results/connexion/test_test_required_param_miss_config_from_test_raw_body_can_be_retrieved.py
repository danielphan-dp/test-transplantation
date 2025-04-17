import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key": "value"}, {"key": "value", "name": "get"}),
    ({}, [{"name": "get"}]),
    ({"another_key": "another_value"}, {"another_key": "another_value", "name": "get"}),
])
def test_get_method_with_kwargs(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method", params=kwargs)
    assert resp.status_code == 200
    assert resp.json == expected

def test_get_method_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method")
    assert resp.status_code == 200
    assert resp.json == [{"name": "get"}]