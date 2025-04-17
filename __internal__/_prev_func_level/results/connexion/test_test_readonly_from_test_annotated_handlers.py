import json
import pytest
from connexion import FlaskJSONProvider
from conftest import build_app_from_fixture

@pytest.fixture
def app(json_datetime_dir, spec, app_class):
    return build_app_from_fixture(json_datetime_dir, app_class=app_class, spec_file=spec, validate_responses=True)

def test_json_method(app):
    app_client = app.test_client()

    # Test valid JSON response
    res = app_client.get("/v1.0/datetime")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert isinstance(data, dict), "Response should be a dictionary"
    assert "value" in data, "Response should contain 'value' key"

    # Test invalid JSON response handling
    res = app_client.get("/v1.0/invalid_endpoint")
    assert res.status_code == 404, f"Error is {res.text}"

    # Test JSON deserialization edge cases
    invalid_json = '{"value": "2000-01-02T03:04:05.000006Z"'
    with pytest.raises(json.JSONDecodeError):
        json.loads(invalid_json)

    # Test empty response
    res = app_client.get("/v1.0/empty")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert data == {}, "Expected empty JSON response"

    # Test response with unexpected data type
    res = app_client.get("/v1.0/uuid")
    assert res.status_code == 200, f"Error is {res.text}"
    data = res.json()
    assert isinstance(data['value'], str), "Expected 'value' to be a string"