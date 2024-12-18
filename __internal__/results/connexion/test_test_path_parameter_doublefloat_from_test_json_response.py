import pytest

@pytest.mark.parametrize('kwargs, expected', [
    ({"arg1": "value1", "arg2": "value2"}, {"arg1": "value1", "arg2": "value2", "name": "get"}),
    ({}, [{"name": "get"}]),
    ({"key": "test"}, {"key": "test", "name": "get"}),
])
def test_get_method(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    response = app_client.get("/v1.0/test-get", query_string=kwargs)
    assert response.status_code == 200
    assert response.json == expected