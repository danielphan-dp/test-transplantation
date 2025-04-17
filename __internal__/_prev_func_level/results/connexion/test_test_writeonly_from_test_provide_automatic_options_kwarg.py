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

    # Test valid post request
    res = app_client.post(
        "/v1.0/user",
        json={"name": "max"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "max"}

    # Test post request with additional unexpected fields
    res = app_client.post(
        "/v1.0/user",
        json={"name": "max", "extra_field": "value"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "max"}

    # Test post request with missing required fields
    res = app_client.post(
        "/v1.0/user",
        json={},
    )
    assert res.status_code == 400  # Assuming the endpoint requires 'name'

    # Test post request with invalid data type
    res = app_client.post(
        "/v1.0/user",
        json={"name": 12345},  # Invalid type for name
    )
    assert res.status_code == 400  # Assuming the endpoint validates types

    # Test post request with empty string for name
    res = app_client.post(
        "/v1.0/user",
        json={"name": ""},
    )
    assert res.status_code == 400  # Assuming empty name is invalid

    # Test post request with a large payload
    large_payload = {"name": "x" * 1000}  # Assuming there's a limit on name length
    res = app_client.post(
        "/v1.0/user",
        json=large_payload,
    )
    assert res.status_code == 201
    assert res.json() == {"name": "x" * 1000}