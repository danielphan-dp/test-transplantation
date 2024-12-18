import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_with_valid_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/json_endpoint",
        json={"key": "value"}
    )
    assert res.status_code == 200
    assert res.json["key"] == "value"

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_with_empty_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/json_endpoint",
        json={}
    )
    assert res.status_code == 200
    assert res.json == {}

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_with_invalid_json(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/json_endpoint",
        data="invalid json"
    )
    assert res.status_code == 400

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_with_large_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    large_data = {"key": "value" * 1000}
    res = app_client.post(
        "/v1.0/json_endpoint",
        json=large_data
    )
    assert res.status_code == 200
    assert res.json["key"] == "value" * 1000

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_with_nested_json(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    nested_data = {"user": {"name": "joe", "age": 20}}
    res = app_client.post(
        "/v1.0/json_endpoint",
        json=nested_data
    )
    assert res.status_code == 200
    assert res.json["user"]["name"] == "joe"
    assert res.json["user"]["age"] == 20