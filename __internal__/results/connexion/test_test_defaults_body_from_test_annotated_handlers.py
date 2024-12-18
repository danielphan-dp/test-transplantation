import json
import pytest
from connexion import App
from connexion.validators.DefaultsJSONRequestBodyValidator import DefaultsJSONRequestBodyValidator

def test_json_method(json_validation_spec_dir, spec):
    """Test the json method for various input scenarios"""

    class MyDefaultsJSONBodyValidator(DefaultsJSONRequestBodyValidator):
        pass

    validator_map = {"body": {"application/json": MyDefaultsJSONBodyValidator}}

    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True, validator_map=validator_map)
    app_client = app.test_client()

    # Test with valid JSON input
    res = app_client.post(
        "/v1.0/user",
        json={"name": "foo"},
    )
    assert res.status_code == 200
    assert res.json().get("human")

    # Test with empty JSON input
    res_empty = app_client.post(
        "/v1.0/user",
        json={},
    )
    assert res_empty.status_code == 400  # Expecting a bad request

    # Test with invalid JSON input
    res_invalid = app_client.post(
        "/v1.0/user",
        data="invalid json",
    )
    assert res_invalid.status_code == 400  # Expecting a bad request

    # Test with missing required fields
    res_missing_field = app_client.post(
        "/v1.0/user",
        json={"age": 30},  # Assuming 'name' is a required field
    )
    assert res_missing_field.status_code == 400  # Expecting a bad request

    # Test with unexpected field
    res_unexpected_field = app_client.post(
        "/v1.0/user",
        json={"name": "foo", "unexpected_field": "bar"},
    )
    assert res_unexpected_field.status_code == 200  # Assuming the API ignores unexpected fields
    assert res_unexpected_field.json().get("human") is not None  # Ensure response is still valid