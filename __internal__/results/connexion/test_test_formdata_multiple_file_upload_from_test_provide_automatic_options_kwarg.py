import pytest
from io import BytesIO

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    resp = app_client.post("/v1.0/post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with single kwarg
    resp = app_client.post("/v1.0/post-method", json={'foo': 'bar'})
    assert resp.status_code == 201
    assert resp.json() == {'foo': 'bar', 'name': 'post'}

    # Test with multiple kwargs
    resp = app_client.post("/v1.0/post-method", json={'foo': 'bar', 'baz': 'qux'})
    assert resp.status_code == 201
    assert resp.json() == {'foo': 'bar', 'baz': 'qux', 'name': 'post'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with unexpected data type
    resp = app_client.post("/v1.0/post-method", json={'foo': 123})
    assert resp.status_code == 201
    assert resp.json() == {'foo': 123, 'name': 'post'}