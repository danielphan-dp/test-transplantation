import pytest

@pytest.mark.parametrize("kwargs, expected", [
    ({"id": 1}, {"id": 1, "name": "get"}),
    ({"name": "test"}, {"name": "test", "name": "get"}),
    ({"foo": "bar"}, {"foo": "bar", "name": "get"}),
])
def test_get_with_kwargs(snake_case_app, kwargs, expected):
    app_client = snake_case_app.test_client()
    resp = app_client.get("/v1.0/test-get-path-snake", query_string=kwargs)
    assert resp.status_code == 200
    assert resp.json() == expected

def test_get_without_kwargs(snake_case_app):
    app_client = snake_case_app.test_client()
    resp = app_client.get("/v1.0/test-get-path-snake")
    assert resp.status_code == 200
    assert resp.json() == [{"name": "get"}]