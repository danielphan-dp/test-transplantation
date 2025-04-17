import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({"key1": "value1", "key2": "value2"}, {"key1": "value1", "key2": "value2", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method_with_kwargs(secure_endpoint_app, kwargs, expected):
    app_client = secure_endpoint_app.test_client()
    response = app_client.get("/v1.0/get", query_string=kwargs)
    assert response.json == expected

def test_get_method_no_kwargs(secure_endpoint_app):
    app_client = secure_endpoint_app.test_client()
    response = app_client.get("/v1.0/get")
    assert response.json == [{"name": "get"}]