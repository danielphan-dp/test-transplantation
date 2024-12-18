import pytest
from connexion import App

def test_post_method_with_valid_data(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"name": "foo"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "foo"}

def test_post_method_with_missing_name(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "post"}

def test_post_method_with_additional_fields(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"name": "foo", "extra_field": "bar"},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "foo"}

def test_post_method_with_invalid_json(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        data="invalid_json",
    )
    assert res.status_code == 400

def test_post_method_with_empty_request(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json=None,
    )
    assert res.status_code == 400