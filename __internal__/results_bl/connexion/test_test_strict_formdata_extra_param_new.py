import json
import pytest

def test_json_method_with_valid_data(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-formData-param", data={"formData": "valid"})
    assert resp.status_code == 200
    assert resp.json() == {"formData": "valid"}

def test_json_method_with_empty_data(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-formData-param", data={})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Missing required formData parameter"

def test_json_method_with_invalid_json(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-formData-param", data="invalid_json")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Invalid JSON format"

def test_json_method_with_extra_parameters(strict_app):
    app_client = strict_app.test_client()
    resp = app_client.post("/v1.0/test-formData-param", data={"formData": "test", "extra_param": "test"})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Extra formData parameter(s) extra_param not in spec"