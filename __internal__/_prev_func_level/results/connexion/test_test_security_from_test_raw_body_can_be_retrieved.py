import pytest

def test_get_method_with_kwargs(secure_endpoint_app):
    app_client = secure_endpoint_app.test_client()
    
    # Test with valid kwargs
    response_with_kwargs = app_client.get("/v1.0/get", query_string={"key": "value"})
    assert response_with_kwargs.status_code == 200
    assert response_with_kwargs.json() == {'key': 'value', 'name': 'get'}

    # Test with multiple kwargs
    response_with_multiple_kwargs = app_client.get("/v1.0/get", query_string={"key1": "value1", "key2": "value2"})
    assert response_with_multiple_kwargs.status_code == 200
    assert response_with_multiple_kwargs.json() == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

    # Test with no kwargs
    response_no_kwargs = app_client.get("/v1.0/get")
    assert response_no_kwargs.status_code == 200
    assert response_no_kwargs.json() == [{'name': 'get'}]

    # Test with empty kwargs
    response_empty_kwargs = app_client.get("/v1.0/get", query_string={})
    assert response_empty_kwargs.status_code == 200
    assert response_empty_kwargs.json() == [{'name': 'get'}]