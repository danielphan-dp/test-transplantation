import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

@pytest.mark.parametrize('data,expected', [
    (json.dumps({"name": "alice", "age": 25}), {"name": "alice-reply", "age": 35}),
    (json.dumps({"name": "bob", "age": 30}), {"name": "bob-reply", "age": 40}),
    (json.dumps({"name": "", "age": 0}), {"name": "empty-reply", "age": 10}),
    (json.dumps({"name": "charlie", "age": -5}), {"name": "charlie-reply", "age": 5}),
])
def test_json_response(json_validation_spec_dir, spec, app_class, data, expected):
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
        data={"x": data},
    )
    assert res.status_code == 200
    assert res.json()["name"] == expected["name"]
    assert res.json()["age"] == expected["age"]

def test_json_invalid_input(json_validation_spec_dir, spec, app_class):
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
        data={"x": "invalid json"},
    )
    assert res.status_code == 400
    assert "error" in res.json()  # Assuming the API returns an error key for invalid input