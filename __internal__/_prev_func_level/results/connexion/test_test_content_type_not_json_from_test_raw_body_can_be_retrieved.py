import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.get("/v1.0/blob-response?param1=value1&param2=value2")
    assert resp.status_code == 200
    
    try:
        content = resp.content
    except AttributeError:
        content = resp.data

    assert isinstance(content, dict)
    assert content['name'] == 'get'
    assert 'param1' in content
    assert content['param1'] == 'value1'
    assert 'param2' in content
    assert content['param2'] == 'value2'

def test_get_without_kwargs(simple_app):
    app_client = simple_app.test_client()
    
    resp = app_client.get("/v1.0/blob-response")
    assert resp.status_code == 200
    
    try:
        content = resp.content
    except AttributeError:
        content = resp.data

    assert isinstance(content, list)
    assert len(content) == 1
    assert content[0]['name'] == 'get'