import json
import pytest

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    response_no_kwargs = app_client.post("/v1.0/greeting/")
    assert response_no_kwargs.status_code == 201
    assert response_no_kwargs.json() == {'name': 'post'}

    # Test with additional kwargs
    response_with_kwargs = app_client.post("/v1.0/greeting/", json={'extra': 'data'})
    assert response_with_kwargs.status_code == 201
    assert response_with_kwargs.json() == {'extra': 'data', 'name': 'post'}

    # Test with different data types in kwargs
    response_with_different_types = app_client.post("/v1.0/greeting/", json={'number': 42, 'flag': True})
    assert response_with_different_types.status_code == 201
    assert response_with_different_types.json() == {'number': 42, 'flag': True, 'name': 'post'}

    # Test with empty data
    response_empty_data = app_client.post("/v1.0/greeting/", json={})
    assert response_empty_data.status_code == 201
    assert response_empty_data.json() == {'name': 'post'}