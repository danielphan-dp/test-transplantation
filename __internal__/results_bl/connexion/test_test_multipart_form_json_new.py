import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_multipart_form_json_empty_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/multipart_form_json",
        files={"file": b""},
        data={"x": json.dumps({})},
    )
    assert res.status_code == 400  # Expecting a bad request for empty JSON
    assert "error" in res.json()

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_multipart_form_json_invalid_json(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/multipart_form_json",
        files={"file": b""},
        data={"x": "invalid_json"},
    )
    assert res.status_code == 400  # Expecting a bad request for invalid JSON
    assert "error" in res.json()

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_multipart_form_json_large_data(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    large_data = json.dumps({"name": "joe", "age": 20} * 1000)  # Large payload
    res = app_client.post(
        "/v1.0/multipart_form_json",
        files={"file": b""},
        data={"x": large_data},
    )
    assert res.status_code == 200
    assert res.json()["name"] == "joe-reply"
    assert res.json()["age"] == 30

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_multipart_form_json_missing_file(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/multipart_form_json",
        data={"x": json.dumps({"name": "joe", "age": 20})},
    )
    assert res.status_code == 400  # Expecting a bad request for missing file
    assert "error" in res.json()