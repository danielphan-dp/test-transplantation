import json
import pytest
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
        "/v1.0/json_method",
        json={"name": "alice", "age": 25},
    )
    assert res.status_code == 200
    assert res.json()["name"] == "alice-reply"
    assert res.json()["age"] == 35

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
        "/v1.0/json_method",
        json={},
    )
    assert res.status_code == 400
    assert "error" in res.json()

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_with_invalid_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/json_method",
        json={"name": 123, "age": "twenty"},
    )
    assert res.status_code == 400
    assert "error" in res.json()