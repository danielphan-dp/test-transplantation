import pytest

def test_put_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no arguments
    resp = app_client.put("/v1.0/nullable-parameters")
    assert resp.json() == {'name': 'put'}
    assert resp.status_code == 201

    # Test with additional keyword arguments
    resp = app_client.put("/v1.0/nullable-parameters", data={"extra_param": "value"})
    assert resp.json() == {'name': 'put', 'extra_param': 'value'}
    assert resp.status_code == 201

    # Test with empty data
    resp = app_client.put("/v1.0/nullable-parameters", data={})
    assert resp.json() == {'name': 'put'}
    assert resp.status_code == 201

    # Test with unexpected data type
    resp = app_client.put("/v1.0/nullable-parameters", data={"post_param": 123})
    assert resp.json() == {'name': 'put', 'post_param': 123}
    assert resp.status_code == 201

    # Test with a large payload
    large_data = {"key": "value" * 1000}
    resp = app_client.put("/v1.0/nullable-parameters", data=large_data)
    assert resp.json() == {'name': 'put', 'key': 'value' * 1000}
    assert resp.status_code == 201

    # Test with invalid endpoint
    resp = app_client.put("/v1.0/nonexistent-endpoint")
    assert resp.status_code == 404