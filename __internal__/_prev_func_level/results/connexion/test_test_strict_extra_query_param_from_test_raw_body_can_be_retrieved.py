import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"param1": "value1"}, {"name": "get", "param1": "value1"}),
    ({"param2": "value2"}, {"name": "get", "param2": "value2"}),
    ({"param1": "value1", "param2": "value2"}, {"name": "get", "param1": "value1", "param2": "value2"}),
])
def test_get_with_kwargs(strict_app, kwargs, expected):
    app_client = strict_app.test_client()
    response = app_client.get("/v1.0/test_endpoint", query_string=kwargs)
    assert response.status_code == 200
    assert response.json() == expected

def test_get_without_kwargs(strict_app):
    app_client = strict_app.test_client()
    response = app_client.get("/v1.0/test_endpoint")
    assert response.status_code == 200
    assert response.json() == [{'name': 'get'}]