import json
import pytest
from connexion import App

def test_json_method_with_valid_data():
    app = App(__name__)
    app_client = app.test_client()
    
    response = app_client.post(
        "/v1.0/user",
        json={"name": "foo"},
    )
    
    assert response.status_code == 200
    assert response.json().get("human") is not None

def test_json_method_with_invalid_data():
    app = App(__name__)
    app_client = app.test_client()
    
    response = app_client.post(
        "/v1.0/user",
        json={"name": None},
    )
    
    assert response.status_code == 400
    assert "error" in response.json()

def test_json_method_with_empty_body():
    app = App(__name__)
    app_client = app.test_client()
    
    response = app_client.post(
        "/v1.0/user",
        json={},
    )
    
    assert response.status_code == 400
    assert "error" in response.json()

def test_json_method_with_non_json_content():
    app = App(__name__)
    app_client = app.test_client()
    
    response = app_client.post(
        "/v1.0/user",
        data="This is not JSON",
        content_type='text/plain'
    )
    
    assert response.status_code == 415
    assert "error" in response.json()