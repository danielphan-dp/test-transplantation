import json
import pytest

def test_post_with_empty_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", data={})
    assert response.status_code == 201
    assert response.json == {'name': 'post'}

def test_post_with_additional_kwargs(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", data={'extra': 'value'})
    assert response.status_code == 201
    assert response.json == {'name': 'post', 'extra': 'value'}

def test_post_with_no_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodday/dan")
    assert response.status_code == 201
    assert response.json == {'name': 'post'}

def test_post_with_invalid_data(simple_app):
    app_client = simple_app.test_client()
    response = app_client.post("/v1.0/goodday/dan", data='invalid data')
    assert response.status_code == 400  # Assuming the method should return a 400 for invalid data

def test_post_with_large_data(simple_app):
    app_client = simple_app.test_client()
    large_data = {f'key_{i}': 'value' for i in range(1000)}
    response = app_client.post("/v1.0/goodday/dan", data=large_data)
    assert response.status_code == 201
    assert response.json == {'name': 'post', **large_data}