import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

def test_post_method(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    # Test with valid input
    res = app_client.post(
        "/v1.0/user",
        json={"name": "max", "password": "1234"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "post", "password": "1234"}

    # Test with missing name
    res = app_client.post(
        "/v1.0/user",
        json={"password": "1234"},
    )
    assert res.status_code == 400  # Assuming the API requires 'name'

    # Test with empty body
    res = app_client.post(
        "/v1.0/user",
        json={},
    )
    assert res.status_code == 400  # Assuming the API requires 'name'

    # Test with additional unexpected fields
    res = app_client.post(
        "/v1.0/user",
        json={"name": "max", "password": "1234", "extra_field": "value"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "post", "password": "1234", "extra_field": "value"}

    # Test with different valid input
    res = app_client.post(
        "/v1.0/user",
        json={"name": "john", "password": "abcd"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "post", "password": "abcd"}