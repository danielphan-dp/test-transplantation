import pytest

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    resp = app_client.post("/v1.0/post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with additional kwargs
    resp = app_client.post("/v1.0/post-method", json={'foo': 'a', 'bar': 'b'})
    assert resp.status_code == 201
    assert resp.json() == {'foo': 'a', 'bar': 'b', 'name': 'post'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with unexpected data type
    resp = app_client.post("/v1.0/post-method", json="string_instead_of_dict")
    assert resp.status_code == 400  # Assuming the endpoint should return a 400 for invalid input

    # Test with large payload
    large_payload = {f'key_{i}': f'value_{i}' for i in range(1000)}
    resp = app_client.post("/v1.0/post-method", json=large_payload)
    assert resp.status_code == 201
    assert resp.json() == {**large_payload, 'name': 'post'}