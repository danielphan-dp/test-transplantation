import json
import pytest
from connexion import App

@pytest.fixture
def app():
    app = App(__name__)
    return app

def test_json_method_with_valid_json(app):
    app_client = app.test_client()
    valid_json = '{"key": "value"}'
    response = app_client.post("/v1.0/test_json", data=valid_json, content_type='application/json')
    
    assert response.status_code == 200
    assert response.json == {"key": "value"}

def test_json_method_with_invalid_json(app):
    app_client = app.test_client()
    invalid_json = '{"key": "value"'
    response = app_client.post("/v1.0/test_json", data=invalid_json, content_type='application/json')
    
    assert response.status_code == 400
    assert response.json["detail"] == "Invalid JSON"

def test_json_method_with_empty_body(app):
    app_client = app.test_client()
    response = app_client.post("/v1.0/test_json", data='', content_type='application/json')
    
    assert response.status_code == 400
    assert response.json["detail"] == "Empty body"

def test_json_method_with_non_json_content(app):
    app_client = app.test_client()
    response = app_client.post("/v1.0/test_json", data='Not a JSON', content_type='text/plain')
    
    assert response.status_code == 415
    assert response.json["detail"] == "Unsupported Media Type"