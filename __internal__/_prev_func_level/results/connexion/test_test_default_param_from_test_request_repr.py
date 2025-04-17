import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({'key1': 'value1'}, {'key1': 'value1', 'name': 'get'}),
    ({'key2': 'value2', 'key3': 'value3'}, {'key2': 'value2', 'key3': 'value3', 'name': 'get'}),
    ({}, [{'name': 'get'}])
])
def test_get_method_with_kwargs(strict_app, kwargs, expected):
    app_client = strict_app.test_client()
    resp = app_client.get("/v1.0/test-get-method", query_string=kwargs)
    assert resp.status_code == 200
    response = resp.json()
    assert response == expected