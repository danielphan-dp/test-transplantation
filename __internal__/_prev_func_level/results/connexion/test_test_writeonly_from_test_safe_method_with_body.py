import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

def test_json_method_with_valid_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"name": "max", "password": "1234"},
    )
    assert res.status_code == 200
    assert "password" not in res.json()

    res = app_client.get("/v1.0/user")
    assert res.status_code == 200
    assert "password" not in res.json()

def test_json_method_with_invalid_json(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        data="invalid json",
        content_type='application/json'
    )
    assert res.status_code == 400
    assert res.json["detail"].startswith("Invalid JSON")

def test_json_method_with_empty_body(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={},
    )
    assert res.status_code == 400
    assert res.json["detail"].startswith("Missing required fields")

def test_json_method_with_non_json_content(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        data="This is not JSON",
        content_type='text/plain'
    )
    assert res.status_code == 415
    assert res.json["detail"].startswith("Unsupported Media Type")