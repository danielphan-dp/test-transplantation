import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key": "value"}, {"key": "value", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_httpstatus_response", query_string=kwargs)
    assert resp.status_code == 200
    assert resp.json == expected

def test_get_method_with_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get_httpstatus_response")
    assert resp.status_code == 200
    assert resp.json == [{"name": "get"}]