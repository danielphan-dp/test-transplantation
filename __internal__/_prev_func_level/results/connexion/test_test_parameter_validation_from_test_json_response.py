import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({"key1": "value1", "key2": "value2"}, {"key1": "value1", "key2": "value2", "name": "get"}),
])
def test_get_with_kwargs(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    url = "/v1.0/test_get_with_kwargs"
    
    response = app_client.get(url, params=kwargs)
    assert response.status_code == 200
    assert response.json == expected

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    url = "/v1.0/test_get_without_kwargs"
    
    response = app_client.get(url)
    assert response.status_code == 200
    assert response.json == [{"name": "get"}]