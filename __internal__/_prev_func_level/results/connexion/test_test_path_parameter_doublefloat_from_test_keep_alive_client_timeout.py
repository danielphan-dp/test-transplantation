import pytest

@pytest.mark.parametrize('kwargs, expected', [
    ({"arg1": "value1", "arg2": "value2"}, {"arg1": "value1", "arg2": "value2", "name": "get"}),
    ({}, [{"name": "get"}]),
    ({"arg": "test"}, {"arg": "test", "name": "get"}),
])
def test_get_method_with_kwargs(simple_app, kwargs, expected):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string=kwargs)
    assert resp.json == expected

@pytest.mark.parametrize('kwargs', [
    ({"arg1": None}),
    ({"arg2": ""}),
])
def test_get_method_with_edge_cases(simple_app, kwargs):
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/test-get", query_string=kwargs)
    assert resp.status_code == 200  # Ensure the method handles edge cases without errors
    assert isinstance(resp.json, list)  # Check that the response is a list when no valid kwargs are provided