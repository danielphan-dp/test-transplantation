import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

def test_post_method_with_valid_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"name": "max"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "max"}

def test_post_method_with_empty_data(json_validation_spec_dir, spec, app_class):
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
    assert res.status_code == 201
    assert res.json() == {"name": "post"}

def test_post_method_with_additional_fields(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"name": "max", "extra_field": "value"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "max"}

def test_post_method_with_invalid_json(json_validation_spec_dir, spec, app_class):
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
    )
    assert res.status_code == 400

def test_post_method_with_missing_name(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"password": "1234"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "post"}