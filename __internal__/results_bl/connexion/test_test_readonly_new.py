import json
import pytest
from connexion import FlaskJSONProvider
from conftest import build_app_from_fixture

def test_json_method_with_valid_data(json_datetime_dir, spec, app_class):
    app = build_app_from_fixture(json_datetime_dir, app_class=app_class, spec_file=spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.get("/v1.0/datetime")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    json_data = json.loads(data['value'])
    assert isinstance(json_data, dict), "Expected JSON data to be a dictionary"

def test_json_method_with_invalid_json(json_datetime_dir, spec, app_class):
    app = build_app_from_fixture(json_datetime_dir, app_class=app_class, spec_file=spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.get("/v1.0/invalid-json")
    assert res.status_code == 400, f"Error is {res.text}"

def test_json_method_with_empty_response(json_datetime_dir, spec, app_class):
    app = build_app_from_fixture(json_datetime_dir, app_class=app_class, spec_file=spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.get("/v1.0/empty")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert data == {}, "Expected empty JSON response"

def test_json_method_with_nonexistent_endpoint(json_datetime_dir, spec, app_class):
    app = build_app_from_fixture(json_datetime_dir, app_class=app_class, spec_file=spec, validate_responses=True)
    app_client = app.test_client()

    res = app_client.get("/v1.0/nonexistent")
    assert res.status_code == 404, f"Error is {res.text}"