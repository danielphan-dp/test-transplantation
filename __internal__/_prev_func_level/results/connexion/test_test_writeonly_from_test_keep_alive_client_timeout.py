import pytest
from connexion import App
from conftest import build_app_from_fixture

@pytest.fixture
def app(json_validation_spec_dir, spec, app_class):
    return build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )

def test_get_with_kwargs(app):
    app_client = app.test_client()
    res = app_client.get("/v1.0/user", query_string={"key": "value"})
    assert res.status_code == 200
    assert res.json() == {"key": "value", "name": "get"}

def test_get_without_kwargs(app):
    app_client = app.test_client()
    res = app_client.get("/v1.0/user")
    assert res.status_code == 200
    assert res.json() == [{"name": "get"}]

def test_get_with_empty_kwargs(app):
    app_client = app.test_client()
    res = app_client.get("/v1.0/user", query_string={})
    assert res.status_code == 200
    assert res.json() == [{"name": "get"}]

def test_get_with_multiple_kwargs(app):
    app_client = app.test_client()
    res = app_client.get("/v1.0/user", query_string={"key1": "value1", "key2": "value2"})
    assert res.status_code == 200
    assert res.json() == {"key1": "value1", "key2": "value2", "name": "get"}