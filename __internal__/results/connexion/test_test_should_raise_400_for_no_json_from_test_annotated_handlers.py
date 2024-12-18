import json
import pytest

def test_should_raise_400_for_invalid_json(simple_app):
    app_client = simple_app.test_client()
    invalid_json_data = "{invalid_json}"
    response = app_client.post("/v1.0/test-invalid-json", data=invalid_json_data, content_type='application/json')
    assert response.status_code == 400
    assert response.json["detail"] == "Invalid JSON format"

def test_should_raise_400_for_non_json_content(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/test-non-json-content", data="This is not JSON", content_type='text/plain')
    assert response.status_code == 400
    assert response.json["detail"] == "Request body must be JSON"

def test_should_return_json_for_valid_request(simple_app):
    app_client = simple_app.test_client()
    valid_json_data = '{"key": "value"}'
    response = app_client.post("/v1.0/test-valid-json", data=valid_json_data, content_type='application/json')
    assert response.status_code == 200
    assert response.json == {"key": "value"}