import pytest
from unittest.mock import Mock
from connexion import FlaskApp

def test_post_method_with_kwargs(app, client):
    """Test post method with various kwargs."""
    app_client = app.test_client()
    
    # Test with no kwargs
    response = app_client.post("/v1.0/post")
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with additional kwargs
    response = app_client.post("/v1.0/post", json={'extra': 'value'})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'extra': 'value'}

    # Test with multiple kwargs
    response = app_client.post("/v1.0/post", json={'foo': 'bar', 'baz': 'qux'})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'foo': 'bar', 'baz': 'qux'}

    # Test with empty kwargs
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with invalid method
    response = app_client.get("/v1.0/post")
    assert response.status_code == 405

    # Test with unexpected data type
    response = app_client.post("/v1.0/post", json="invalid_data")
    assert response.status_code == 400  # Assuming the API returns 400 for invalid JSON data