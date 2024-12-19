import json
import pytest
from pathlib import Path
from connexion import App
from connexion.json_schema import Draft4RequestValidator
from connexion.spec import Specification
from connexion.validators import DefaultsJSONRequestBodyValidator, JSONRequestBodyValidator
from jsonschema.validators._utils import extend
from jsonschema.validators import Draft4Validator
from conftest import build_app_from_fixture

def test_json_method_empty_string(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"name": "max", "password": ""},
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid password"

def test_json_method_invalid_json(json_validation_spec_dir, spec, app_class):
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
    assert res.json()["detail"] == "Invalid JSON"

def test_json_method_missing_fields(json_validation_spec_dir, spec, app_class):
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
    assert res.status_code == 400
    assert res.json()["detail"] == "Missing password field"

def test_json_method_successful_response(json_validation_spec_dir, spec, app_class):
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