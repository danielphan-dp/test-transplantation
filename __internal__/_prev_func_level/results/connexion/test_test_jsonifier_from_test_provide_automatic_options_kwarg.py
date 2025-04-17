import pytest

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    response = app_client.post("/v1.0/post")
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}

    # Test with additional kwargs
    response = app_client.post("/v1.0/post", json={'extra': 'data'})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'extra': 'data'}

    # Test with different types of kwargs
    response = app_client.post("/v1.0/post", json={'number': 123, 'boolean': True})
    assert response.status_code == 201
    assert response.json() == {'name': 'post', 'number': 123, 'boolean': True}

    # Test with empty kwargs
    response = app_client.post("/v1.0/post", json={})
    assert response.status_code == 201
    assert response.json() == {'name': 'post'}