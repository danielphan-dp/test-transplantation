import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_empty_string(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/multipart_form_json_array",
        files={"file": b""},
        data={"x": ""}
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid JSON input"

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_invalid_json(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/multipart_form_json_array",
        files={"file": b""},
        data={"x": "invalid_json"}
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid JSON input"

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_large_json_array(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    large_data = json.dumps([{"name": "user" + str(i), "age": i} for i in range(1000)])
    res = app_client.post(
        "/v1.0/multipart_form_json_array",
        files={"file": b""},
        data={"x": large_data}
    )
    assert res.status_code == 200
    assert len(res.json()) == 1000

@pytest.mark.parametrize('spec', ['openapi.yaml'])
def test_json_method_malformed_json(json_validation_spec_dir, spec, app_class):
    app = build_app_from_fixture(
        json_validation_spec_dir,
        app_class=app_class,
        spec_file=spec,
        validate_responses=True,
    )
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/multipart_form_json_array",
        files={"file": b""},
        data={"x": json.dumps([{"name": "joe", "age": 20}, {"name": "alena", "age": 28,])}]}  # Malformed JSON
    )
    assert res.status_code == 400
    assert res.json()["detail"] == "Invalid JSON input"