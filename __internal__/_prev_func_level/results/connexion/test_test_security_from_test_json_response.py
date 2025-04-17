import pytest

def test_get_method_with_kwargs(secure_endpoint_app):
    app_client = secure_endpoint_app.test_client()

    # Test with valid kwargs
    response_with_kwargs = app_client.get("/v1.0/get-method", query_string={'key1': 'value1', 'key2': 'value2'})
    assert response_with_kwargs.status_code == 200
    assert response_with_kwargs.json == {'key1': 'value1', 'key2': 'value2', 'name': 'get'}

    # Test with empty kwargs
    response_empty_kwargs = app_client.get("/v1.0/get-method")
    assert response_empty_kwargs.status_code == 200
    assert response_empty_kwargs.json == [{'name': 'get'}]

    # Test with single kwarg
    response_single_kwarg = app_client.get("/v1.0/get-method", query_string={'key1': 'value1'})
    assert response_single_kwarg.status_code == 200
    assert response_single_kwarg.json == {'key1': 'value1', 'name': 'get'}

    # Test with unexpected kwarg
    response_unexpected_kwarg = app_client.get("/v1.0/get-method", query_string={'unexpected_key': 'unexpected_value'})
    assert response_unexpected_kwarg.status_code == 200
    assert response_unexpected_kwarg.json == {'unexpected_key': 'unexpected_value', 'name': 'get'}

    # Test with multiple kwargs
    response_multiple_kwargs = app_client.get("/v1.0/get-method", query_string={'key1': 'value1', 'key2': 'value2', 'key3': 'value3'})
    assert response_multiple_kwargs.status_code == 200
    assert response_multiple_kwargs.json == {'key1': 'value1', 'key2': 'value2', 'key3': 'value3', 'name': 'get'}