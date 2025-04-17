import pytest
from io import BytesIO

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()

    # Test with no kwargs
    resp = app_client.post("/v1.0/test-post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with single kwarg
    resp = app_client.post("/v1.0/test-post-method", json={'key1': 'value1'})
    assert resp.status_code == 201
    assert resp.json() == {'key1': 'value1', 'name': 'post'}

    # Test with multiple kwargs
    resp = app_client.post("/v1.0/test-post-method", json={'key1': 'value1', 'key2': 'value2'})
    assert resp.status_code == 201
    assert resp.json() == {'key1': 'value1', 'key2': 'value2', 'name': 'post'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/test-post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}