import pytest
from conftest import build_app_from_fixture

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2"}, {"key2": "value2", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method(json_datetime_dir, spec, app_class, kwargs, expected):
    app = build_app_from_fixture(
        json_datetime_dir, app_class=app_class, spec_file=spec, validate_responses=True
    )
    app_client = app.test_client()

    res = app_client.get("/v1.0/test_endpoint", query_string=kwargs)
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert data == expected

def test_get_method_no_kwargs(json_datetime_dir, spec, app_class):
    app = build_app_from_fixture(
        json_datetime_dir, app_class=app_class, spec_file=spec, validate_responses=True
    )
    app_client = app.test_client()

    res = app_client.get("/v1.0/test_endpoint")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert data == [{"name": "get"}]