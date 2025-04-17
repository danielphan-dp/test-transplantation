import pytest
from flask import Flask

@pytest.mark.parametrize('path', ['/', '/home', '/bp/', '/view', '/methodview'])
def test_post_method(path, async_app):
    test_client = async_app.test_client()
    headers = {"Content-type": "application/json"}
    
    # Test POST request with valid data
    response = test_client.post(path, headers=headers, json={"data": "valid"})
    assert response.data == b'Create'
    
    # Test POST request with no data
    response = test_client.post(path, headers=headers, json={})
    assert response.data == b'Create'
    
    # Test POST request with invalid data type
    response = test_client.post(path, headers=headers, json={"data": 123})
    assert response.data == b'Create'
    
    # Test POST request with unexpected path
    response = test_client.post('/unexpected_path', headers=headers, json={"data": "valid"})
    assert response.status_code == 404

    # Test GET request to ensure it does not interfere with POST
    response = test_client.get(path)
    assert b"GET" in response.get_data()