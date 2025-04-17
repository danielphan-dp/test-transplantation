import pytest
from io import BytesIO

def test_post_method_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    # Test with no kwargs
    resp = app_client.post("/v1.0/test-post-method")
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with additional kwargs
    resp = app_client.post("/v1.0/test-post-method", json={"foo": "bar", "baz": "qux"})
    assert resp.status_code == 201
    assert resp.json() == {'foo': 'bar', 'baz': 'qux', 'name': 'post'}

    # Test with empty kwargs
    resp = app_client.post("/v1.0/test-post-method", json={})
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}

    # Test with unexpected data type
    resp = app_client.post("/v1.0/test-post-method", data="string_instead_of_json")
    assert resp.status_code == 400  # Assuming the endpoint expects JSON and returns 400 for invalid data

    # Test with file upload
    resp = app_client.post(
        "/v1.0/test-post-method",
        data={"file": ("filename.txt", BytesIO(b"file contents"))}
    )
    assert resp.status_code == 201
    assert resp.json() == {'name': 'post'}  # Assuming the file upload does not affect the response structure