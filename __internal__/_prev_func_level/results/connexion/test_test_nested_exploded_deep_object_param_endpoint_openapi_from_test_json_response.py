import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"param": "test"}, {"param": "test", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method(simple_openapi_app, kwargs, expected):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/get", query_string=kwargs)
    assert response.status_code == 200
    assert response.json == expected