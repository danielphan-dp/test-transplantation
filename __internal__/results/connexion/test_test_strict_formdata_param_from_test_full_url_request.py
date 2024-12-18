import pytest

def test_post_method_with_kwargs(strict_app):
    app_client = strict_app.test_client()
    url = "/v1.0/test_post_method"
    
    # Test with no kwargs
    resp = app_client.post(url)
    response = resp.json()
    assert response == {'name': 'post'}
    assert resp.status_code == 201

    # Test with additional kwargs
    resp = app_client.post(url, json={"extra_param": "value"})
    response = resp.json()
    assert response == {'name': 'post', 'extra_param': 'value'}
    assert resp.status_code == 201

    # Test with multiple kwargs
    resp = app_client.post(url, json={"param1": "value1", "param2": "value2"})
    response = resp.json()
    assert response == {'name': 'post', 'param1': 'value1', 'param2': 'value2'}
    assert resp.status_code == 201

    # Test with empty kwargs
    resp = app_client.post(url, json={})
    response = resp.json()
    assert response == {'name': 'post'}
    assert resp.status_code == 201

    # Test with invalid data type
    resp = app_client.post(url, json="invalid_data")
    assert resp.status_code == 400  # Assuming the endpoint returns 400 for invalid data type