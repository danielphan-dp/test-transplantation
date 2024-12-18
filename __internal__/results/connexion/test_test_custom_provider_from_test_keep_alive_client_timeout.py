import pytest
from connexion.FlaskApp import FlaskApp
from conftest import build_app_from_fixture

@pytest.mark.parametrize("kwargs, expected", [
    ({"key1": "value1"}, {"key1": "value1", "name": "get"}),
    ({"key2": "value2", "key3": "value3"}, {"key2": "value2", "key3": "value3", "name": "get"}),
    ({}, [{"name": "get"}])
])
def test_get_method_with_kwargs(spec, kwargs, expected):
    simple_flask_app = build_app_from_fixture(
        "simple", app_class=FlaskApp, spec_file=spec, validate_responses=True
    )
    flask_app = simple_flask_app.app
    app_client = simple_flask_app.test_client()

    resp = app_client.get("/v1.0/get-method", query_string=kwargs)
    assert resp.status_code == 200
    response = resp.json()
    assert response == expected