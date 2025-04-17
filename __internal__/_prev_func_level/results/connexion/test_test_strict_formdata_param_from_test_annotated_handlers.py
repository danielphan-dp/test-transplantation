import json
import pytest

def test_json_method_with_valid_json(strict_app):
    app_client = strict_app.test_client()
    url = "/v1.0/test_json"
    valid_json_data = json.dumps({"key": "value"})
    resp = app_client.post(url, data=valid_json_data, content_type='application/json')
    response = resp.json()
    assert response == {"key": "value"}
    assert resp.status_code == 200

def test_json_method_with_invalid_json(strict_app):
    app_client = strict_app.test_client()
    url = "/v1.0/test_json"
    invalid_json_data = "{key: value}"  # Invalid JSON format
    resp = app_client.post(url, data=invalid_json_data, content_type='application/json')
    assert resp.status_code == 400

def test_json_method_with_empty_json(strict_app):
    app_client = strict_app.test_client()
    url = "/v1.0/test_json"
    empty_json_data = json.dumps({})
    resp = app_client.post(url, data=empty_json_data, content_type='application/json')
    response = resp.json()
    assert response == {}
    assert resp.status_code == 200

def test_json_method_with_non_json_data(strict_app):
    app_client = strict_app.test_client()
    url = "/v1.0/test_json"
    non_json_data = "This is not JSON"
    resp = app_client.post(url, data=non_json_data, content_type='text/plain')
    assert resp.status_code == 400

def test_json_method_with_large_json(strict_app):
    app_client = strict_app.test_client()
    url = "/v1.0/test_json"
    large_json_data = json.dumps({"key": "value" * 1000})  # Large JSON object
    resp = app_client.post(url, data=large_json_data, content_type='application/json')
    response = resp.json()
    assert response == {"key": "value" * 1000}
    assert resp.status_code == 200