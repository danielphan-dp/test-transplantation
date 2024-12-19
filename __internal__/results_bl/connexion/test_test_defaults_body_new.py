import json
import pytest
from connexion import App
from connexion.validators.DefaultsJSONRequestBodyValidator import DefaultsJSONRequestBodyValidator

def test_json_method_empty_body(json_validation_spec_dir, spec):
    """Test json method with an empty body"""
    
    class MyDefaultsJSONBodyValidator(DefaultsJSONRequestBodyValidator):
        pass

    validator_map = {"body": {"application/json": MyDefaultsJSONBodyValidator}}

    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True, validator_map=validator_map)
    app_client = app.test_client()

    res = app_client.post("/v1.0/user", json={})
    assert res.status_code == 400  # Expecting a bad request due to empty body

def test_json_method_invalid_json(json_validation_spec_dir, spec):
    """Test json method with invalid JSON"""
    
    class MyDefaultsJSONBodyValidator(DefaultsJSONRequestBodyValidator):
        pass

    validator_map = {"body": {"application/json": MyDefaultsJSONBodyValidator}}

    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True, validator_map=validator_map)
    app_client = app.test_client()

    res = app_client.post("/v1.0/user", data="invalid json")
    assert res.status_code == 400  # Expecting a bad request due to invalid JSON

def test_json_method_missing_key(json_validation_spec_dir, spec):
    """Test json method with missing required key"""
    
    class MyDefaultsJSONBodyValidator(DefaultsJSONRequestBodyValidator):
        pass

    validator_map = {"body": {"application/json": MyDefaultsJSONBodyValidator}}

    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True, validator_map=validator_map)
    app_client = app.test_client()

    res = app_client.post("/v1.0/user", json={"age": 30})  # Missing 'name' key
    assert res.status_code == 400  # Expecting a bad request due to missing required key

def test_json_method_successful_case(json_validation_spec_dir, spec):
    """Test json method with valid input"""
    
    class MyDefaultsJSONBodyValidator(DefaultsJSONRequestBodyValidator):
        pass

    validator_map = {"body": {"application/json": MyDefaultsJSONBodyValidator}}

    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True, validator_map=validator_map)
    app_client = app.test_client()

    res = app_client.post("/v1.0/user", json={"name": "foo"})
    assert res.status_code == 200
    assert res.json().get("human") is not None  # Ensure 'human' key is present in response

def test_json_method_extra_keys(json_validation_spec_dir, spec):
    """Test json method with extra keys in the body"""
    
    class MyDefaultsJSONBodyValidator(DefaultsJSONRequestBodyValidator):
        pass

    validator_map = {"body": {"application/json": MyDefaultsJSONBodyValidator}}

    app = App(__name__, specification_dir=json_validation_spec_dir)
    app.add_api(spec, validate_responses=True, validator_map=validator_map)
    app_client = app.test_client()

    res = app_client.post("/v1.0/user", json={"name": "foo", "extra_key": "extra_value"})
    assert res.status_code == 200
    assert res.json().get("human") is not None  # Ensure 'human' key is present in response