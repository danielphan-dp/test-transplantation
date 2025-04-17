import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"id": 1}, {"name": "get", "id": 1}),
    ({"foo": "bar"}, {"name": "get", "foo": "bar"}),
    ({}, [{"name": "get"}])
])
def test_get_method_with_kwargs(simple_openapi_app, kwargs, expected):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/get", query_string=kwargs)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == expected

def test_get_method_no_kwargs(simple_openapi_app):
    app_client = simple_openapi_app.test_client()
    response = app_client.get("/v1.0/get")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data == [{"name": "get"}]