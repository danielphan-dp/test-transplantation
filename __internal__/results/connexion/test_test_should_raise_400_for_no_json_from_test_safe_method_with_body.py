import json
import pytest

def test_should_raise_400_for_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json_data = "{invalid_json}"
    response = app_client.post("/v1.0/test-invalid-json", data=invalid_json_data, content_type='application/json')
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid JSON format"

def test_should_return_json_for_valid_request(simple_app):
    app_client = simple_app.test_client()
    valid_json_data = json.dumps({"key": "value"})
    response = app_client.post("/v1.0/test-valid-json", data=valid_json_data, content_type='application/json')
    assert response.status_code == 200
    assert response.json() == {"key": "value"}

def test_should_raise_400_for_empty_json(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-empty-json", data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    assert response.json()["detail"] == "Request body must not be empty"