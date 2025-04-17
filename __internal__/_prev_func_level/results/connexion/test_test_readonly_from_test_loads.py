import json
import pytest
from connexion import FlaskJSONProvider
from conftest import build_app_from_fixture

def test_json_method(json_datetime_dir, spec, app_class):
    app = build_app_from_fixture(
        json_datetime_dir, app_class=app_class, spec_file=spec, validate_responses=True
    )
    app_client = app.test_client()

    res = app_client.get("/v1.0/" + spec.replace("yaml", "json"))
    assert res.status_code == 200, f"Error is {res.text}"
    spec_data = res.json()

    def get_value(data, path):
        for part in path.split("."):
            data = data.get(part)
            assert data, f"No data in part '{part}' of '{path}'"
        return data

    example = get_value(spec_data, f"paths./datetime.get.responses.200.content.application/json.schema.example.value")
    assert example in [
        "2000-01-23T04:56:07.000008+00:00",
        "2000-01-23T04:56:07.000008Z",
    ]
    
    res = app_client.get("/v1.0/datetime")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert data == {"value": "2000-01-02T03:04:05.000006Z"}

    res = app_client.get("/v1.0/invalid_endpoint")
    assert res.status_code == 404, f"Expected 404 for invalid endpoint, got {res.status_code}"

    res = app_client.get("/v1.0/date")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert data == {"value": "2000-01-02"}

    res = app_client.get("/v1.0/uuid")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert data == {"value": "e7ff66d0-3ec2-4c4e-bed0-6e4723c24c51"}

    invalid_json = b'{"invalid": "json"'
    with pytest.raises(json.JSONDecodeError):
        json.loads(invalid_json)