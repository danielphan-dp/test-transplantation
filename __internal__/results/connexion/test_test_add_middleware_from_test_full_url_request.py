import pytest
from unittest.mock import Mock
from connexion import FlaskApp

def test_post_method_with_valid_kwargs():
    app = FlaskApp(__name__)
    app.add_url_rule('/post', view_func=app.post)
    
    app_client = app.test_client()
    response = app_client.post('/post', json={'key': 'value'})
    
    assert response.status_code == 201
    assert response.json == {'key': 'value', 'name': 'post'}

def test_post_method_with_empty_kwargs():
    app = FlaskApp(__name__)
    app.add_url_rule('/post', view_func=app.post)
    
    app_client = app.test_client()
    response = app_client.post('/post', json={})
    
    assert response.status_code == 201
    assert response.json == {'name': 'post'}

def test_post_method_with_additional_kwargs():
    app = FlaskApp(__name__)
    app.add_url_rule('/post', view_func=app.post)
    
    app_client = app.test_client()
    response = app_client.post('/post', json={'extra': 'data'})
    
    assert response.status_code == 201
    assert response.json == {'extra': 'data', 'name': 'post'}

def test_post_method_with_invalid_data():
    app = FlaskApp(__name__)
    app.add_url_rule('/post', view_func=app.post)
    
    app_client = app.test_client()
    response = app_client.post('/post', data='invalid data')
    
    assert response.status_code == 400  # Assuming the app handles invalid data with a 400 response

def test_post_method_with_large_payload():
    app = FlaskApp(__name__)
    app.add_url_rule('/post', view_func=app.post)
    
    large_payload = {f'key_{i}': f'value_{i}' for i in range(1000)}
    app_client = app.test_client()
    response = app_client.post('/post', json=large_payload)
    
    assert response.status_code == 201
    assert response.json['name'] == 'post'
    assert len(response.json) == 1001  # 1000 keys + 'name' key