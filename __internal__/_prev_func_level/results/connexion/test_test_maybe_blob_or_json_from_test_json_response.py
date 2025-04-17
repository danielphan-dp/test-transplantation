import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get", query_string=kwargs)
    
    assert resp.status_code == 200
    assert resp.json == expected

def test_get_method_no_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get")
    
    assert resp.status_code == 200
    assert resp.json == [{"name": "get"}]