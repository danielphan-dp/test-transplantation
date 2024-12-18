import pytest

@pytest.mark.parametrize('kwargs, expected', [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2", "key3": "value3"}, {"key2": "value2", "key3": "value3", "name": "get"}),
    ({}, [{'name': 'get'}]),
])
def test_get_method_with_kwargs(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string=kwargs)
    assert resp.json == expected
    assert isinstance(resp.json, dict) if kwargs else isinstance(resp.json, list)