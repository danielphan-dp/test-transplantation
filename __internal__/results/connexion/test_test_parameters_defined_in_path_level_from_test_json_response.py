import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"title": "nice-get"}, {"name": "get", "title": "nice-get"}),
    ({}, [{"name": "get"}]),
    ({"extra": "value"}, {"name": "get", "extra": "value"}),
])
def test_get_method_with_parameters(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-method", query_string=kwargs)
    assert resp.status_code == 200
    assert resp.json() == expected

def test_get_method_without_parameters(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get-method")
    assert resp.status_code == 200
    assert resp.json() == [{"name": "get"}]