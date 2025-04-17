import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

def test_json_method(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    # Test valid JSON input
    res = app_client.post(
        "/v1.0/user",
        json={"name": "max", "password": "1234"},
    )
    assert res.status_code == 200
    assert "password" not in res.json()

    # Test invalid JSON input
    res = app_client.post(
        "/v1.0/user",
        json={"name": "max", "password": None},
    )
    assert res.status_code == 400
    assert res.json()["detail"].startswith("Invalid input")

    # Test empty JSON input
    res = app_client.post(
        "/v1.0/user",
        json={},
    )
    assert res.status_code == 400
    assert res.json()["detail"].startswith("Missing required fields")

    # Test JSON deserialization
    res = app_client.get("/v1.0/user")
    assert res.status_code == 200
    assert "password" not in res.json()

    # Test error handling for invalid JSON response
    res = app_client.get("/v1.0/user_with_password")
    assert res.status_code == 500
    assert res.json()["detail"].startswith(
        "Response body does not conform to specification"
    )