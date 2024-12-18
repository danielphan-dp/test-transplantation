import pytest

def test_get_with_kwargs(simple_app):
    """Test get method with kwargs provided."""
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get?param1=value1&param2=value2")
    assert resp.status_code == 200
    assert resp.json() == {'name': 'get', 'param1': 'value1', 'param2': 'value2'}

def test_get_without_kwargs(simple_app):
    """Test get method without kwargs provided."""
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get")
    assert resp.status_code == 200
    assert resp.json() == [{'name': 'get'}]

def test_get_with_empty_kwargs(simple_app):
    """Test get method with empty kwargs."""
    app_client = simple_app.test_client()
    resp = app_client.get("/v1.0/get?param1=")
    assert resp.status_code == 200
    assert resp.json() == {'name': 'get', 'param1': ''}