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
    assert res.json() == {"name": "foo", "name": "post"}

def test_post_method_with_empty_data(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={},
    )
    assert res.status_code == 201
    assert res.json() == {"name": "post"}

def test_post_method_with_invalid_data(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"invalid_key": "value"},
    )
    assert res.status_code == 201
    assert res.json() == {"invalid_key": "value", "name": "post"}

def test_post_method_with_missing_key(json_validation_spec_dir, spec):
    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.post(
        "/v1.0/user",
        json={"name": None},
    )
    assert res.status_code == 201
    assert res.json() == {"name": None, "name": "post"}