import json
import pytest

def test_json_method_with_valid_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-formData-param", data={"formData": "valid test"})
    assert resp.status_code == 200
    response = resp.json()
    assert response == "valid test"

def test_json_method_with_empty_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-formData-param", data={"formData": ""})
    assert resp.status_code == 200
    response = resp.json()
    assert response == ""

def test_json_method_with_invalid_json(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-formData-param", data={"formData": "{invalid_json}"})
    assert resp.status_code == 400

def test_json_method_with_non_string_data(simple_app):
    app_client = simple_app.test_client()
    resp = app_client.post("/v1.0/test-formData-param", data={"formData": 12345})
    assert resp.status_code == 200
    response = resp.json()
    assert response == 12345

def test_json_method_with_large_data(simple_app):
    app_client = simple_app.test_client()
    large_data = "a" * 10000
    resp = app_client.post("/v1.0/test-formData-param", data={"formData": large_data})
    assert resp.status_code == 200
    response = resp.json()
    assert response == large_data