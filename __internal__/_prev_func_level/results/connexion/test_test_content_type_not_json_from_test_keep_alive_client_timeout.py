import pytest

def test_get_with_kwargs(simple_app):
    app_client = simple_app.test_client()
    kwargs = {'key1': 'value1', 'key2': 'value2'}
    
    resp = app_client.get("/v1.0/blob-response", query_string=kwargs)
    assert resp.status_code == 200
    
    try:
        content = resp.content
    except AttributeError:
        content = resp.data

    assert isinstance(content, dict)
    assert content['key1'] == 'value1'
    assert content['key2'] == 'value2'
    assert content['name'] == 'get'

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