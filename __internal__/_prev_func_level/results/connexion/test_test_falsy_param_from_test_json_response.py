import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"key": "value"}, {"key": "value", "name": "get"}),
    ({}, [{"name": "get"}]),
    ({"another_key": "another_value"}, {"another_key": "another_value", "name": "get"}),
])
def test_get_method(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method", params=kwargs)
    assert resp.status_code == 200
    response = resp.json()
    assert response == expected

def test_get_method_no_params(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get-method")
    assert resp.status_code == 200
    response = resp.json()
    assert response == [{"name": "get"}]