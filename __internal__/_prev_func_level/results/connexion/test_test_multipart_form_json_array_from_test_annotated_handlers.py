import json
import pytest
from connexion import App
from conftest import build_app_from_fixture

@pytest.mark.parametrize('data,expected', [
    (json.dumps({"name": "joe", "age": 20}), {"name": "joe-reply", "age": 30}),
    (json.dumps({"name": "alena", "age": 28}), {"name": "alena-reply", "age": 38}),
    (json.dumps({"name": "invalid", "age": "not_a_number"}), None),  # Edge case with invalid age
])
def test_json_method(json_validation_spec_dir, spec, app_class, data, expected):
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
        data={"x": data},
    )
    
    if expected is not None:
        assert res.status_code == 200
        assert res.json()[0]["name"] == expected["name"]
        assert res.json()[0]["age"] == expected["age"]
    else:
        assert res.status_code == 400  # Expecting a bad request for invalid data