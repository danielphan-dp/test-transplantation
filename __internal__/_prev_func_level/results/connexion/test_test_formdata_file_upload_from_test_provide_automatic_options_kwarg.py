import pytest
from io import BytesIO

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()

    # Test with no kwargs
    resp = app_client.post("/v1.0/post-method")
    assert resp.status_code == 200
    assert resp.json() == {'name': 'post'}

    # Test with additional kwargs
    resp = app_client.post("/v1.0/post-method", json={'foo': 'bar'})
    assert resp.status_code == 200
    assert resp.json() == {'foo': 'bar', 'name': 'post'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/post-method", json={})
    assert resp.status_code == 200
    assert resp.json() == {'name': 'post'}

    # Test with unexpected data type
    resp = app_client.post("/v1.0/post-method", data="string_instead_of_json")
    assert resp.status_code == 400

    # Test with invalid JSON
    resp = app_client.post("/v1.0/post-method", data='{"foo": "bar",}')
    assert resp.status_code == 400

    # Test with large payload
    large_payload = {'data': 'x' * 10000}
    resp = app_client.post("/v1.0/post-method", json=large_payload)
    assert resp.status_code == 200
    assert resp.json() == {'data': 'x' * 10000, 'name': 'post'}