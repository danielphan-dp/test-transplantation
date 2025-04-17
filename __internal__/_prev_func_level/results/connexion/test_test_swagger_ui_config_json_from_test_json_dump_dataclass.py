import json
import pytest
from connexion import App

def test_json_method_with_valid_data(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app.add_api(spec)
    app_client = app.test_client()
    
    valid_json_data = '{"key": "value"}'
    response = app_client.post('/v1.0/json', data=valid_json_data, content_type='application/json')
    
    assert response.status_code == 200
    assert response.json == json.loads(valid_json_data)

def test_json_method_with_invalid_data(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app.add_api(spec)
    app_client = app.test_client()
    
    invalid_json_data = '{"key": "value"'
    response = app_client.post('/v1.0/json', data=invalid_json_data, content_type='application/json')
    
    assert response.status_code == 400
    assert 'error' in response.json

def test_json_method_with_empty_data(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app.add_api(spec)
    app_client = app.test_client()
    
    empty_json_data = ''
    response = app_client.post('/v1.0/json', data=empty_json_data, content_type='application/json')
    
    assert response.status_code == 400
    assert 'error' in response.json

def test_json_method_with_non_json_data(simple_api_spec_dir, spec):
    app = App(__name__, specification_dir=simple_api_spec_dir)
    app.add_api(spec)
    app_client = app.test_client()
    
    non_json_data = 'This is not JSON'
    response = app_client.post('/v1.0/json', data=non_json_data, content_type='text/plain')
    
    assert response.status_code == 400
    assert 'error' in response.json