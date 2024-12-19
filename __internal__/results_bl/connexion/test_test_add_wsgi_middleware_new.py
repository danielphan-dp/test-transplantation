import pytest
from unittest.mock import Mock
from connexion import FlaskApp

def test_post_method_with_valid_kwargs():
    app = FlaskApp(__name__)
    client = app.test_client()
    
    response = client.post("/v1.0/greeting/robbe", json={"key": "value"})
    
    assert response.status_code == 201
    assert response.json == {'name': 'post', 'key': 'value'}

def test_post_method_with_empty_kwargs():
    app = FlaskApp(__name__)
    client = app.test_client()
    
    response = client.post("/v1.0/greeting/robbe", json={})
    
    assert response.status_code == 201
    assert response.json == {'name': 'post'}

def test_post_method_with_additional_kwargs():
    app = FlaskApp(__name__)
    client = app.test_client()
    
    response = client.post("/v1.0/greeting/robbe", json={"extra": "data"})
    
    assert response.status_code == 201
    assert response.json == {'name': 'post', 'extra': 'data'}

def test_post_method_with_invalid_data():
    app = FlaskApp(__name__)
    client = app.test_client()
    
    response = client.post("/v1.0/greeting/robbe", data="invalid data")
    
    assert response.status_code == 400  # Assuming the endpoint returns 400 for invalid data

def test_post_method_with_large_payload():
    app = FlaskApp(__name__)
    client = app.test_client()
    
    large_payload = {f'key_{i}': 'value' for i in range(1000)}
    response = client.post("/v1.0/greeting/robbe", json=large_payload)
    
    assert response.status_code == 201
    assert response.json['name'] == 'post'
    assert len(response.json) == 1001  # 1000 keys + 'name' key