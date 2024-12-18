import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({"key1": "value1", "key2": "value2"}, {"key1": "value1", "key2": "value2", "name": "get"}),
])
def test_get_with_kwargs(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", params=kwargs)
    assert resp.status_code == 200
    response = resp.json()
    assert response == expected

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get")
    assert resp.status_code == 200
    response = resp.json()
    assert response == [{'name': 'get'}]