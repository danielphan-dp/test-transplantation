import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_post_method_with_valid_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/post",
        json={"name": "test_name", "age": 25},
    )
    assert res.status_code == 201
    assert res.json["name"] == "test_name"
    assert "age" not in res.json  # age is not returned

def test_post_method_with_empty_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/post",
        json={},
    )
    assert res.status_code == 201
    assert res.json["name"] == "post"  # default name when no data is provided

def test_post_method_with_invalid_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/post",
        json={"invalid_key": "value"},
    )
    assert res.status_code == 201
    assert res.json["name"] == "post"  # default name when invalid data is provided

def test_post_method_with_large_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    large_data = {"name": "a" * 1000}  # large name
    res = app_client.post(
        "/v1.0/post",
        json=large_data,
    )
    assert res.status_code == 201
    assert res.json["name"] == "a" * 1000  # check if large data is handled correctly