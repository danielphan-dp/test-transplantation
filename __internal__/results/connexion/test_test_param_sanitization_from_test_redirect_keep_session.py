import pytest

def test_post_method(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    resp = app_client.post("/v1.0/post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with additional kwargs
    resp = app_client.post("/v1.0/post-method", json={"key1": "value1", "key2": "value2"})
    assert resp.status_code == 201
    assert resp.json() == {'key1': 'value1', 'key2': 'value2', 'name': 'post'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with unexpected data type
    resp = app_client.post("/v1.0/post-method", json={"key1": 123, "key2": [1, 2, 3]})
    assert resp.status_code == 201
    assert resp.json() == {'key1': 123, 'key2': [1, 2, 3], 'name': 'post'}

    # Test with large payload
    large_payload = {f'key{i}': f'value{i}' for i in range(1000)}
    resp = app_client.post("/v1.0/post-method", json=large_payload)
    assert resp.status_code == 201
    assert resp.json() == {**large_payload, 'name': 'post'}