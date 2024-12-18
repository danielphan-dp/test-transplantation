import json
import pytest
from connexion import App

def test_json_method_with_valid_json():
    """Test json method with valid JSON input."""
    app = App(__name__)
    app_client = app.test_client()
    valid_json = '{"key": "value"}'
    response = app_client.post('/v1.0/test-json', data=valid_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == json.loads(valid_json)

def test_json_method_with_invalid_json():
    """Test json method with invalid JSON input."""
    app = App(__name__)
    app_client = app.test_client()
    invalid_json = '{"key": "value"'
    response = app_client.post('/v1.0/test-json', data=invalid_json, content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_empty_string():
    """Test json method with empty string input."""
    app = App(__name__)
    app_client = app.test_client()
    response = app_client.post('/v1.0/test-json', data='', content_type='application/json')
    assert response.status_code == 400

def test_json_method_with_non_json_data():
    """Test json method with non-JSON data."""
    app = App(__name__)
    app_client = app.test_client()
    non_json_data = 'Just a plain string'
    response = app_client.post('/v1.0/test-json', data=non_json_data, content_type='text/plain')
    assert response.status_code == 400

def test_json_method_with_large_json():
    """Test json method with large JSON input."""
    app = App(__name__)
    app_client = app.test_client()
    large_json = json.dumps({"key": "value" * 10000})
    response = app_client.post('/v1.0/test-json', data=large_json, content_type='application/json')
    assert response.status_code == 200
    assert response.json == json.loads(large_json)