import pytest
from flask import Flask

@pytest.mark.parametrize('path', ['/', '/home', '/bp/', '/view', '/methodview'])
def test_post_route(path, async_app):
    test_client = async_app.test_client()
    headers = {"Content-type": "application/json"}
    
    # Test POST request with valid data
    response = test_client.post(path, headers=headers, json={"data": "test"})
    assert response.status_code == 200
    assert b"Create" in response.get_data()

    # Test POST request with missing data
    response = test_client.post(path, headers=headers, json={})
    assert response.status_code == 400  # Assuming the endpoint requires data

    # Test GET request to ensure it does not interfere with POST
    response = test_client.get(path)
    assert b"GET" in response.get_data()