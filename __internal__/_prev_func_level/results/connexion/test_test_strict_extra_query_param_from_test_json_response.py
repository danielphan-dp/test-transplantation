import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"param1": "value1"}, {"name": "get", "param1": "value1"}),
    ({"param2": "value2"}, {"name": "get", "param2": "value2"}),
    ({"param1": "value1", "param2": "value2"}, {"name": "get", "param1": "value1", "param2": "value2"}),
])
def test_get_with_kwargs(strict_app, kwargs, expected):
    app_client = strict_app.test_client()
    resp = app_client.get("/v1.0/test_get", query_string=kwargs)
    assert resp.status_code == 200
    response = resp.json()
    assert response == expected

def test_get_without_kwargs(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.get("/v1.0/test_get")
    assert resp.status_code == 200
    response = resp.json()
    assert response == [{"name": "get"}]