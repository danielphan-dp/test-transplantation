import pytest

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    resp = app_client.post("/v1.0/post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with additional kwargs
    resp = app_client.post("/v1.0/post-method", json={'extra': 'data'})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'extra': 'data'}

    # Test with multiple kwargs
    resp = app_client.post("/v1.0/post-method", json={'foo': 'bar', 'baz': 'qux'})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post', 'foo': 'bar', 'baz': 'qux'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}