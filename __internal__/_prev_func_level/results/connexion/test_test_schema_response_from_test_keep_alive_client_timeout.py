import pytest

def test_get_method_with_kwargs(schema_app):
    app_client = schema_app.test_client()
    
    # Test with valid kwargs
    request = app_client.get("/v1.0/test_get_method", query_string={"key": "value"})
    assert request.status_code == 200, request.text
    assert request.json == {'key': 'value', 'name': 'get'}

    # Test with multiple kwargs
    request = app_client.get("/v1.0/test_get_method", query_string={"key1": "value1", "key2": "value2"})
    assert request.status_code == 200, request.text
    assert request.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

    # Test with no kwargs
    request = app_client.get("/v1.0/test_get_method")
    assert request.status_code == 200, request.text
    assert request.json == [{'name': 'get'}]

    # Test with empty kwargs
    request = app_client.get("/v1.0/test_get_method", query_string={})
    assert request.status_code == 200, request.text
    assert request.json == [{'name': 'get'}]