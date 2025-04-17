import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({"key1": "value1", "key2": "value2"}, {"key1": "value1", "key2": "value2", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method_with_kwargs(secure_endpoint_app, kwargs, expected):
    app_client = secure_endpoint_app.test_client()
    response = app_client.get("/v1.0/more-than-one-scope", query_string=kwargs)
    assert response.json == expected
    assert response.status_code == 200 if kwargs else 200

def test_get_method_no_kwargs(secure_endpoint_app):
    app_client = secure_endpoint_app.test_client()
    response = app_client.get("/v1.0/more-than-one-scope")
    assert response.json == [{"name": "get"}]
    assert response.status_code == 200

def test_get_method_with_empty_kwargs(secure_endpoint_app):
    app_client = secure_endpoint_app.test_client()
    response = app_client.get("/v1.0/more-than-one-scope", query_string={})
    assert response.json == [{"name": "get"}]
    assert response.status_code == 200