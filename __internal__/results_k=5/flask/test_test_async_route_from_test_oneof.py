import pytest
from flask import Flask, jsonify

@pytest.mark.parametrize('path', ['/', '/home', '/bp/', '/view', '/methodview'])
def test_post_method(path, async_app):
    test_client = async_app.test_client()
    
    # Test valid POST request
    response = test_client.post(path)
    assert response.data == b'Create'
    
    # Test response status code
    assert response.status_code == 200
    
    # Test content type
    assert response.headers.get("content-type") == "text/html; charset=utf-8"
    
    # Test invalid POST request with additional data
    response = test_client.post(path, json={"invalid": "data"})
    assert response.data == b'Create'
    assert response.status_code == 200

    # Test POST with no data
    response = test_client.post(path, data={})
    assert response.data == b'Create'
    assert response.status_code == 200