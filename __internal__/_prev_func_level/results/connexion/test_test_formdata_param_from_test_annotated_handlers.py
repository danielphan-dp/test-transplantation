import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    valid_json = '{"key": "value"}'
    resp = app_client.post("/v1.0/test-json", data=valid_json, content_type='application/json')
    assert resp.status_code == 200
    response = resp.json()
    assert response == {"key": "value"}

    # Test with invalid JSON string
    invalid_json = '{"key": "value"'
    resp = app_client.post("/v1.0/test-json", data=invalid_json, content_type='application/json')
    assert resp.status_code == 400
    response = resp.json()
    assert "error" in response

    # Test with empty JSON
    empty_json = '{}'
    resp = app_client.post("/v1.0/test-json", data=empty_json, content_type='application/json')
    assert resp.status_code == 200
    response = resp.json()
    assert response == {}

    # Test with non-JSON data
    non_json_data = "This is not JSON"
    resp = app_client.post("/v1.0/test-json", data=non_json_data, content_type='text/plain')
    assert resp.status_code == 400
    response = resp.json()
    assert "error" in response