import json
import pytest

def test_json_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with valid JSON string
    resp = app_client.post("/v1.0/test-json", data=json.dumps({"key": "value"}), content_type='application/json')
    assert resp.status_code == 200, resp.text
    response = resp.json()
    assert response == {"key": "value"}

    # Test with invalid JSON string
    resp = app_client.post("/v1.0/test-json", data="invalid json", content_type='application/json')
    assert resp.status_code == 400, resp.text

    # Test with empty JSON
    resp = app_client.post("/v1.0/test-json", data=json.dumps({}), content_type='application/json')
    assert resp.status_code == 200, resp.text
    response = resp.json()
    assert response == {}

    # Test with nested JSON
    resp = app_client.post("/v1.0/test-json", data=json.dumps({"nested": {"key": "value"}}), content_type='application/json')
    assert resp.status_code == 200, resp.text
    response = resp.json()
    assert response == {"nested": {"key": "value"}}