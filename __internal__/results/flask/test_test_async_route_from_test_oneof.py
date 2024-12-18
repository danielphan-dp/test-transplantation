import pytest
from flask import Flask, jsonify

@pytest.mark.parametrize('path', ['/', '/home', '/bp/', '/view', '/methodview'])
def test_post_route(path, async_app):
    test_client = async_app.test_client()
    
    # Test POST request without data
    response = test_client.post(path)
    assert response.data == b'Create'
    
    # Test POST request with data
    response = test_client.post(path, json={"key": "value"})
    assert response.data == b'Create'
    
    # Test POST request with invalid data
    response = test_client.post(path, json={"invalid": "data"})
    assert response.data == b'Create'